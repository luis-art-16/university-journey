"""
Módulo Principal da Camada de Ligação de Dados (Data Link Layer).
Integra as subcamadas de MAC, Deteção/Correção de Erros (FEC/CRC)
e Controlo de Fluxo (ARQ Stop-and-Wait).
"""
import time
import os
from logger import gerar_log

# ==========================================
# Dependências do Protocolo
# ==========================================
from constantes_protocolo import TYPE_TEXT, TYPE_IMAGE, MIN_PAYLOAD_SIZE, MAX_PAYLOAD_SIZE, TYPE_EOF
from framing_hdlc import byte_stuffing, byte_destuffing, SOF
from camada_fisica import Camada2_FullDuplex
from encapsulamento import encapsular_trama
from crc8 import calcular_crc8, verificar_crc8
from maquina_estados_arq import MaquinaEstadosARQ
from temporizador_arq import GestorTimeout
from fec_hamming import codificar_hamming, decodificar_hamming

class CamadaDeLigacao:
    def __init__(self, porta_com='COM3'):
        gerar_log("SISTEMA", f"A inicializar a Camada de Ligação de Dados na porta {porta_com}...", "INFO")
        
        # Inicialização dos sub-módulos de rede
        self.link = Camada2_FullDuplex(porta_com, baudrate=9600)
        self.arq = MaquinaEstadosARQ()
        self.gestor_timeout = GestorTimeout(timeout_segundos=2.0, max_tentativas=7)

        self.buffer_rececao = bytearray()
        self.ultimo_tempo_rececao = time.time()

    def iniciar_ligacao(self):
        """Ativa a interface de hardware e prepara o canal lógico."""
        self.link.iniciar()

    def fechar_ligacao(self):
        """Termina o processo com segurança, libertando recursos."""
        self.link.parar()

    # ==========================================
    # FLUXO DE TRANSMISSÃO
    # ==========================================
    def enviar_ficheiro(self, payload: bytes, tipo: int) -> bool: ##
        """
        Ponto de acesso (API) para a Camada de Aplicação.
        Gere o encapsulamento, proteção FEC e garante a entrega através do mecanismo ARQ.
        """
        tamanho = len(payload)
        if not (MIN_PAYLOAD_SIZE <= tamanho <= MAX_PAYLOAD_SIZE):
            gerar_log("ERRO API", f"Tamanho de payload inválido: {tamanho} bytes.", "ERRO")
            return False

        def envio_dados_canal(dados):                  ##
            seq = self.arq.obter_seq_num_atual()       ##1
            
            # Aplicar codificação de canal para correção de erros
            payload_protegido = codificar_hamming(dados) ##2
            
            # Encapsulamento de Cabeçalho
            trama_base = encapsular_trama(payload_protegido, 0x02, 0x01, tipo, seq, b'') ##2
            
            # Cálculo do FCS e delimitação da trama
            fcs = calcular_crc8(trama_base)                                     ##3
            trama_completa = trama_base + fcs                                     ##4
            pacote_fisico = SOF + byte_stuffing(trama_completa) + SOF           ##5
            
            self.link.enviar_trama_fisica(pacote_fisico)                   ##6

        # O gestor de timeout assume o controlo do envio a partir daqui
        return self.gestor_timeout.enviar_e_esperar_ack( ##
            payload, 
            enviar_trama=envio_dados_canal, 
            esperar_ack=self._escutar_canal_arq
        )

    # ==========================================
    # FLUXO DE RECEÇÃO
    # ==========================================
    def _escutar_canal_arq(self): ##
        """
        Processa as tramas que chegam do canal físico.
        Efetua o Destuffing, validação de FCS, correção FEC e processa as regras da máquina de estados.
        """
        if self.link.tramas_recebidas:
            trama_bruta = self.link.tramas_recebidas.pop(0)
            
            # Reverter byte stuffing para recuperar a trama original
            trama_limpa = byte_destuffing(trama_bruta)                        ##1
            
            if len(trama_limpa) < 6:
                return None
                
            fcs_recebido = trama_limpa[-1:]
            dados = trama_limpa[:-1]

    
            crc_valido = verificar_crc8(dados, fcs_recebido)                ##2
            
            if not crc_valido:
                cabecalho = dados[:5]
                payload_corrompido = dados[5:]
                
                # Tentativa de correção de erros com o Código de Hamming
                payload_limpo, erros = decodificar_hamming(payload_corrompido)  ##3
                
                # Revalidação do CRC após correção do payload
                payload_recodificado = codificar_hamming(payload_limpo)
                dados_reconstruidos = cabecalho + payload_recodificado
                
                if verificar_crc8(dados_reconstruidos, fcs_recebido):
                    gerar_log("FEC", f"Recuperados {erros} erro(s) de bit no payload.", "SUCESSO")
                    dados = dados_reconstruidos
                    crc_valido = True
                else:
                    return "NACK" # Erros a mais para o FEC resolver. Pedir retransmissão imediata (NACK).
            
            # Confirmação final da integridade da trama
            if not verificar_crc8(dados, fcs_recebido):
                return "NACK"
                
            tipo = trama_limpa[2]
            seq = trama_limpa[3]
            
            # Processamento de Tramas de Controlo (ACKs recebidos)
            if tipo == 0x0A:
                if self.arq.processar_ack_recebido(seq):       ##
                    return "ACK"                               ##
                return None

            # Processamento de Tramas de Dados (Payload / EOF)
            elif tipo in [TYPE_TEXT, TYPE_IMAGE, TYPE_EOF]:
                acao = self.arq.avaliar_trama_recebida(seq) ##4
                
                # Preparação do ACK de resposta
                ack_header = self.arq.gerar_trama_ack(seq)  ##5
                ack_fcs = calcular_crc8(ack_header)         ##6
                ack_pacote = SOF + byte_stuffing(ack_header + ack_fcs) + SOF
                
                if acao == "ACEITAR_E_ENVIAR_ACK":
                    self.ultimo_tempo_rececao = time.time()
                    
                    # Processamento da flag de fim de transferência (EOF)
                    if tipo == TYPE_EOF:
                        length = trama_limpa[4]
                        len_real = 256 if length == 0 else length
                        payload_protegido = trama_limpa[5:5+len_real]
                        
                        payload_extensao, _ = decodificar_hamming(payload_protegido)
                        extensao = payload_extensao.decode('utf-8', errors='ignore').strip()
                        
                        if not extensao.startswith('.'):
                            extensao = ".bin"

                        dados_finais = bytes(self.buffer_rececao)
                        tamanho = len(dados_finais)
                        
                        nome_guardar = f"ficheiro_recebido_{int(time.time())}{extensao}"
                        
                        if tamanho > 0:
                            os.makedirs("ficheiros_recebidos", exist_ok=True)
                            caminho_completo = os.path.join("ficheiros_recebidos", nome_guardar)

                            with open(caminho_completo, 'wb') as f:
                                f.write(dados_finais)
                            gerar_log("SISTEMA", f"Sessão concluída. Ficheiro ({tamanho} bytes) gravado em '{caminho_completo}'.", "SUCESSO")
                            
                        # Reposição de estado para a próxima transferência
                        self.buffer_rececao.clear() 
                        self.arq.seq_num_esperado = 0 
                        gerar_log("SISTEMA", "Máquina de estados reposta. A aguardar novos dados.", "INFO")

                    # Processamento de trama de dados normal
                    else:
                        length = trama_limpa[4]
                        len_real = 256 if length == 0 else length
                        payload_protegido = trama_limpa[5:5+len_real]
                        
                        payload_final, _ = decodificar_hamming(payload_protegido)
                        self.buffer_rececao.extend(payload_final)
                    
                    self.link.enviar_trama_fisica(ack_pacote)
                    return None
                    
        return None