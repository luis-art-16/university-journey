"""
Módulo de verificação de integridade de dados utilizando CRC-8
(Cyclic Redundancy Check).
"""

def calcular_crc8(dados: bytes) -> bytes:
    """
    Calcula o valor de CRC-8 para um dado conjunto de bytes.
    Utiliza o polinómio gerador padrão 0x07 (x^8 + x^2 + x + 1).
    
    Args:
        dados (bytes): A sequência de bytes a processar.
        
    Returns:
        bytes: O valor de CRC calculado (1 byte).
    """
    crc = 0x00
    polinomio = 0x07
    
    for byte in dados:
        crc ^= byte  # Operação XOR do byte atual com o valor do CRC
        
        # Processamento bit a bit
        for _ in range(8):
            if crc & 0x80:  # Verifica se o bit mais significativo (MSB) é 1
                crc = (crc << 1) ^ polinomio
            else:
                crc = (crc << 1)
                
            crc &= 0xFF  # Garante que o valor não excede 8 bits (1 byte)
            
    return bytes([crc])

def verificar_crc8(dados: bytes, crc_recebido: bytes) -> bool:
    """
    Valida a integridade de uma trama comparando o CRC-8 recalculado
    com o valor de FCS (Frame Check Sequence) recebido.
    
    Args:
        dados (bytes): Os dados base recebidos na trama.
        crc_recebido (bytes): O byte de FCS lido no final da trama.
        
    Returns:
        bool: True se não forem detetados erros, False caso contrário.
    """
    crc_calculado = calcular_crc8(dados)
    return crc_calculado == crc_recebido