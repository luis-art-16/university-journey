"""
Módulo de gestão temporal e retransmissões (Temporizador ARQ).
Implementa o mecanismo de timeout associado ao protocolo Stop-and-Wait
para garantir que a entrega de tramas é bem sucedida.
"""
import time
from logger import gerar_log 

class GestorTimeout:
    def __init__(self, timeout_segundos=1.5, max_tentativas=3):
        """
        Inicializa o gestor de retransmissões.
        
        Args:
            timeout_segundos (float): Tempo limite de espera por um ACK (em segundos).
            max_tentativas (int): Número máximo de tentativas de transmissão antes de declarar falha.
        """
        self.timeout_segundos = timeout_segundos
        self.max_tentativas = max_tentativas

    def enviar_e_esperar_ack(self, trama: bytes, enviar_trama, esperar_ack) -> bool: ## 
        """
        Gere o ciclo de vida de uma trama: transmissão, inicialização do temporizador, 
        avaliação da resposta e acionamento de retransmissões em caso de timeout ou NACK.
        
        Args:
            trama (bytes): A Protocol Data Unit (PDU) a ser transmitida.
            rotina_enviar (callable): Função de envio da trama no canal físico.
            rotina_escutar_ack (callable): Função para verificar a chegada de confirmações no canal.
            
        Returns:
            bool: True se a trama foi confirmada com sucesso, False em caso de falha crítica.
        """
        tentativa_atual = 1

        while tentativa_atual <= self.max_tentativas:
            gerar_log("ARQ", f"Transmissão iniciada (Tentativa {tentativa_atual}/{self.max_tentativas}).", "INFO")
            
            # 1. Envio da trama no meio físico
            enviar_trama(trama)

            # 2. Inicialização do temporizador
            tempo_inicio = time.time()

            # 3. Aguardar resposta do recetor (ACK/NACK)
            while (time.time() - tempo_inicio) < self.timeout_segundos:
                resposta = esperar_ack()                                            ##
                
                if resposta == "ACK":
                    rtt = time.time() - tempo_inicio
                    gerar_log("ARQ", f"Trama confirmada (ACK recebido em {rtt:.2f}s).", "SUCESSO")
                    return True 
                
                elif resposta == "NACK":
                    gerar_log("ARQ", "Trama rejeitada pelo recetor (NACK). A iniciar retransmissão imediata.", "AVISO")
                    time.sleep(0.2)
                    break # Quebra o ciclo de espera para forçar nova tentativa
                
                # Pequena pausa para não sobrecarregar o CPU
                time.sleep(0.01) 

            # Avaliação de Timeout (se sairmos do while sem resposta)
            if resposta != "NACK":
                gerar_log("ARQ", f"Timeout esgotado ({self.timeout_segundos}s) sem resposta. A preparar retransmissão.", "ERRO")
            
            tentativa_atual += 1

        # Limite máximo de transmissões atingido
        gerar_log("ARQ", "Falha de ligação persistente. Limite de retransmissões atingido.", "ERRO")
        return False