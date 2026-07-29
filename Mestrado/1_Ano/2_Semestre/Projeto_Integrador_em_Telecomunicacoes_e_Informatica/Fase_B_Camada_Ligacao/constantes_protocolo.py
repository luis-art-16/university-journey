"""
Módulo de definição das constantes e parâmetros físicos do protocolo.
Baseado nas especificações do relatório técnico do Grupo 3.
"""

# ==========================================
# Tipos de Trama (Campo TYPE do Cabeçalho)
# ==========================================
TYPE_TEXT = 0x01       # Ficheiros de texto / documentos
TYPE_IMAGE = 0x02      # Conteúdos multimédia (imagens, binários)
TYPE_EOF = 0x03        # Flag de terminação de transferência (End of File)

TYPE_ACK = 0x0A        # Controlo: Confirmação positiva (Acknowledge)
TYPE_NACK = 0x0B       # Controlo: Confirmação negativa (Negative Acknowledge)

# ==========================================
# Limites Físicos da Trama (Payload)
# ==========================================
# De acordo com a arquitetura, o campo Length aloca 1 Byte (0-255).
# Por convenção do protocolo, length 0 representa o tamanho máximo (256 bytes).
MIN_PAYLOAD_SIZE = 1   
MAX_PAYLOAD_SIZE = 256





