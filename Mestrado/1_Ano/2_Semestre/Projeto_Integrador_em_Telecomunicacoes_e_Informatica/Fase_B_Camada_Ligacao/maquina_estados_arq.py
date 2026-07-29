"""
Módulo de controlo de fluxo e recuperação de erros.
Implementa a Máquina de Estados para o protocolo ARQ (Automatic Repeat reQuest)
com a variante Stop-and-Wait.
"""

class MaquinaEstadosARQ:
    def __init__(self):
        """
        Inicializa a máquina de estados do protocolo Stop-and-Wait.
        Controla os números de sequência (0 e 1) alternados para sincronização
        entre o emissor e o recetor.
        """
        self.seq_num_enviar = 0    # Número de sequência a anexar à próxima trama a transmitir
        self.seq_num_esperado = 0  # Número de sequência esperado na próxima trama a receber

    # ==========================================
    # LÓGICA DO EMISSOR
    # ==========================================
    def obter_seq_num_atual(self) -> int:
        """Retorna o número de sequência atual (0 ou 1) para o cabeçalho da trama."""
        return self.seq_num_enviar

    def processar_ack_recebido(self, seq_num_ack: int) -> bool:
        """
        Processa a trama de controlo (ACK) recebida.
        Valida se o número de sequência do ACK corresponde à trama transmitida.
        Em caso afirmativo, avança o estado da máquina.
        
        Args:
            seq_num_ack (int): O número de sequência extraído do ACK recebido.
            
        Returns:
            bool: True se o ACK for válido e sincronizado, False caso contrário.
        """
        if seq_num_ack == self.seq_num_enviar:
            # Confirmação válida. Alterna o número de sequência (0 -> 1 ou 1 -> 0).
            self.seq_num_enviar = 1 - self.seq_num_enviar
            return True
        else:
            # ACK duplicado ou não sincronizado. É ignorado pela máquina de estados.
            return False

    # ==========================================
    # LÓGICA DO RECETOR
    # ==========================================
    def avaliar_trama_recebida(self, seq_num_recebido: int) -> str:
        """
        Verifica se a trama que chegou é nova ou repetida (para evitar 
        guardar duas vezes a mesma parte do ficheiro)..
        
        Args:
            seq_num_recebido (int): O número de sequência da trama recém-chegada.
            
        Returns:
            str: Ação de controlo a ser executada pela Camada de Ligação.
        """
        if seq_num_recebido == self.seq_num_esperado:
            # Trama sincronizada. Avança o estado para o próximo número de sequência.
            self.seq_num_esperado = 1 - self.seq_num_esperado
            return "ACEITAR_E_ENVIAR_ACK"
        else:
            # Deteção de pacote duplicado (provável perda do ACK anterior no canal físico).
            # O payload é descartado, mas o ACK deve ser retransmitido para destrancar o emissor.
            return "DESCARTAR_DUPLICADO_MAS_ENVIAR_ACK"

    def gerar_trama_ack(self, seq_num_para_confirmar: int) -> bytes:
        """
        Gera o cabeçalho de uma trama de controlo (ACK) para confirmar
        a receção de uma trama de dados.
        
        Args:
            seq_num_para_confirmar (int): O número de sequência a confirmar.
            
        Returns:
            bytes: O cabeçalho da trama ACK formatado (5 bytes).
        """
        TIPO_ACK = b'\x0A' 
        # Estrutura do Cabeçalho: MAC_Destino(1) + MAC_Origem(1) + TIPO(1) + SEQ(1) + LENGTH(1)
        # O campo Length é 0x00, pois as tramas de controlo não contêm payload de dados.
        cabecalho_ack = b'\x01' + b'\x02' + TIPO_ACK + bytes([seq_num_para_confirmar]) + b'\x00'
        return cabecalho_ack