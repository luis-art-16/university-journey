"""
Módulo responsável pela construção da Trama (Encapsulamento).
Implementa a montagem do cabeçalho (Header) e a junção do campo de verificação de erros (FCS)
ao Protocol Data Unit (PDU) antes da transmissão no canal físico.
"""
import struct

def encapsular_trama(payload: bytes, mac_dest: int, mac_orig: int, tipo: int, seq_num: int, fcs: bytes) -> bytes:
    """
    Recebe os dados da camada superior, insere os campos de controlo e endereço,
    e anexa a cauda (Trailer/FCS).
    """
    # 1. Definição do campo Length (1 byte). 
    # O limite máximo do payload é de 256 bytes. Mapeamento de 256 para 0x00 para o valor caber em 8 bits.
    length_campo = len(payload) % 256 
    
    # 2. Formatação do Cabeçalho (Header)
    # Estrutura do cabeçalho: 5 campos de 1 byte cada, em formato de rede padrão (Big-Endian '>BBBBB')
    # Ordem: Endereço MAC Destino, Endereço MAC Origem, Tipo de Trama, Número de Sequência, Comprimento
    cabecalho = struct.pack(
        '>BBBBB', 
        mac_dest, 
        mac_orig, 
        tipo, 
        seq_num, 
        length_campo
    )
    
    # 3. Montagem da Trama Final (Cabeçalho + Dados + FCS)
    # O enquadramento físico (Byte Stuffing e SOF) será processado e delegado posteriormente ao módulo HDLC.
    trama_encapsulada = cabecalho + payload + fcs
    
    return trama_encapsulada