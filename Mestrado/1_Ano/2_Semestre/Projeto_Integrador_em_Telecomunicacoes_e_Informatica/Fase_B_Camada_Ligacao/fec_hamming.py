"""
Módulo de Forward Error Correction (FEC).
Implementa a codificação e descodificação de canal utilizando o Código de Hamming (7,4).
Permite a deteção e correção automática de erros de bit único por cada nibble transmitido.
"""

def codificar_nibble(nibble: int) -> int:
    """
    Aplica o Código de Hamming (7,4) a um bloco de 4 bits (nibble).
    Calcula os 3 bits de paridade resultantes do cruzamento de dados.
    
    Args:
        nibble (int): Os 4 bits de dados originais.
        
    Returns:
        int: O byte resultante contendo os 4 bits de dados e os 3 de paridade 
             (Formato: 0 | p1 | p2 | d1 | p3 | d2 | d3 | d4).
    """
    d1 = (nibble >> 3) & 1
    d2 = (nibble >> 2) & 1
    d3 = (nibble >> 1) & 1
    d4 = nibble & 1
    
    # Cálculo dos bits de paridade (Equações de Matriz)
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4
    
    return (p1 << 6) | (p2 << 5) | (d1 << 4) | (p3 << 3) | (d2 << 2) | (d3 << 1) | d4

def decodificar_nibble(byte_val: int) -> tuple[int, bool]:
    """
    Descodifica um bloco de 7 bits (Hamming 7,4) e corrige um erro de bit único, se detetado.
    
    Args:
        byte_val (int): O byte recebido contendo o código protegido.
        
    Returns:
        tuple[int, bool]: Tupla com o nibble original corrigido e uma flag 
                          indicando se ocorreu correção matemática.
    """
    p1 = (byte_val >> 6) & 1
    p2 = (byte_val >> 5) & 1
    d1 = (byte_val >> 4) & 1
    p3 = (byte_val >> 3) & 1
    d2 = (byte_val >> 2) & 1
    d3 = (byte_val >> 1) & 1
    d4 = byte_val & 1
    
    # Cálculo do Vetor de Síndrome (Verificação de Integridade)
    s1 = p1 ^ d1 ^ d2 ^ d4
    s2 = p2 ^ d1 ^ d3 ^ d4
    s3 = p3 ^ d2 ^ d3 ^ d4
    
    sindrome = (s3 << 2) | (s2 << 1) | s1
    erro_corrigido = False
    
    if sindrome != 0:
        erro_corrigido = True
        # Correção do bit corrompido com base na posição indicada pela síndrome
        if sindrome == 3: d1 ^= 1
        elif sindrome == 5: d2 ^= 1
        elif sindrome == 6: d3 ^= 1
        elif sindrome == 7: d4 ^= 1
        # Síndromes 1, 2 ou 4 indicam corrupção nos próprios bits de paridade (ignorado)
        
    nibble_corrigido = (d1 << 3) | (d2 << 2) | (d3 << 1) | d4
    return nibble_corrigido, erro_corrigido

def codificar_hamming(dados_originais: bytes) -> bytes:
    """
    Aplica a codificação de canal (Hamming 7,4) a um fluxo completo de bytes.
    A redundância inserida efetua o dobro do overhead do tamanho original do payload.
    
    Args:
        dados_originais (bytes): O payload em dados de aplicação puros.
        
    Returns:
        bytes: O payload codificado e protegido contra ruído.
    """
    codificado = bytearray()
    for byte in dados_originais:
        high = (byte >> 4) & 0x0F
        low = byte & 0x0F
        codificado.append(codificar_nibble(high))
        codificado.append(codificar_nibble(low))
    return bytes(codificado)

def decodificar_hamming(dados_codificados: bytes) -> tuple[bytes, int]:
    """
    Remove a codificação de canal do fluxo recebido e aciona o mecanismo FEC.
    
    Args:
        dados_codificados (bytes): O payload protegido recebido pelo canal físico.
        
    Returns:
        tuple[bytes, int]: Os dados de aplicação reconstruídos e o número 
                           total de erros de bit único mitigados no processo.
    """
    decodificado = bytearray()
    erros = 0
    
    for i in range(0, len(dados_codificados), 2):
        if i + 1 >= len(dados_codificados): break
        
        high_nibble, err1 = decodificar_nibble(dados_codificados[i])
        low_nibble, err2 = decodificar_nibble(dados_codificados[i+1])
        
        if err1: erros += 1
        if err2: erros += 1
        
        decodificado.append((high_nibble << 4) | low_nibble)
        
    return bytes(decodificado), erros