"""
Módulo de delimitação de tramas (Enquadramento).
Garante que os caracteres especiais do protocolo não sejam confundidos 
com os dados reais do utilizador durante a transmissão.
"""
# ==========================================
# Flags de Controlo HDLC
# ==========================================
SOF = b'\x7E'      # Start of Frame (Delimitador)
ESC = b'\x7D'      # Escape Character
ESC_SOF = b'\x5E'  # Substituição para o byte SOF no meio dos dados
ESC_ESC = b'\x5D'  # Substituição para o byte ESC no meio dos dados

def byte_stuffing(frame_data: bytes) -> bytes:
    """
    Aplica o algoritmo de Byte Stuffing à trama de dados.
    Garante que a flag delimitadora (SOF) não surge no meio do payload,
    evitando falsas deteções de fim de trama pelo recetor.
    """
    stuffed_data = bytearray()
    for byte in frame_data:
        b = bytes([byte])
        if b == SOF:
            stuffed_data.extend(ESC + ESC_SOF)
        elif b == ESC:
            stuffed_data.extend(ESC + ESC_ESC)
        else:
            stuffed_data.extend(b)
    return bytes(stuffed_data)

def byte_destuffing(stuffed_data: bytes) -> bytes:
    """
    Reverte o processo de Byte Stuffing na trama recebida.
    Remove os bytes de escape e restaura os dados originais.
    """
    destuffed_data = bytearray()
    escape_next = False
    
    for byte in stuffed_data:
        b = bytes([byte])
        if escape_next:
            if b == ESC_SOF:
                destuffed_data.extend(SOF)
            elif b == ESC_ESC:
                destuffed_data.extend(ESC)
            else:
                # Tolerância a falhas: mantém o byte original se a sequência de escape for inválida
                destuffed_data.extend(b)
            escape_next = False
        elif b == ESC:
            escape_next = True
        else:
            destuffed_data.extend(b)
            
    return bytes(destuffed_data)