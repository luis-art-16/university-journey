"""
Módulo de Teste de Carga e Avaliação de Throughput.
Avalia a capacidade de processamento contínuo e a taxa de sucesso 
na entrega de pacotes através do canal.
"""

import time
from camada_ligacao_dados import CamadaDeLigacao
from constantes_protocolo import TYPE_TEXT
from logger import gerar_log

def modulo_teste_desempenho(camada2, numero_tramas=100): 
    """Envia tráfego "pesado" utilizando a arquitetura integrada para extrair estatísticas de débito.""" 
    gerar_log("TESTE STRESS", f"A iniciar envio de {numero_tramas} tramas para avaliação de carga...", "INFO")
    
    tramas_enviadas = 0 
    tramas_entregues_sucesso = 0 
    
    # Payload gerado artificialmente para simular tráfego útil
    payload_dados = b'\xAA' * 100

    tempo_inicio = time.time() 

    for i in range(numero_tramas): 
        print(f"\n--- A transmitir trama {i+1}/{numero_tramas} ---")
        
        # ABSTRAÇÃO DA CAMADA DE LIGAÇÃO: 
        # A API trata do encapsulamento, CRC, FEC e do controlo ARQ Stop-and-Wait
        sucesso = camada2.enviar_ficheiro(payload=payload_dados, tipo=TYPE_TEXT)
        
        tramas_enviadas += 1 
        
        if sucesso: 
            tramas_entregues_sucesso += 1 
        else: 
            gerar_log("TESTE STRESS", f"Falha na entrega da trama {i+1} após todas as retransmissões.", "ERRO")

    tempo_fim = time.time() 
    
    # Processamento de Métricas e Estatísticas
    duracao_total = tempo_fim - tempo_inicio
    taxa_sucesso = (tramas_entregues_sucesso / numero_tramas) * 100 
    
    # Débito Efetivo (Throughput) = (Tramas entregues * Tamanho do Payload * 8 bits) / Tempo total
    throughput = (tramas_entregues_sucesso * len(payload_dados) * 8) / duracao_total if duracao_total > 0 else 0

    print("\n" + "="*45) 
    print("      RESULTADOS DA AVALIAÇÃO DE DESEMPENHO      ") 
    print("="*45) 
    print(f"Tempo Total Gasto:         {duracao_total:.2f} segundos") 
    print(f"Tramas Entregues:          {tramas_entregues_sucesso}/{numero_tramas}")
    print(f"Taxa de Sucesso:       {taxa_sucesso:.1f}%") 
    print(f"Débito Efetivo (Prático):  {throughput:.2f} bps") 
    print("="*45) 

if __name__ == "__main__": 
    PORTA_ESP32 = 'COM3'  
    
    camada2 = CamadaDeLigacao(porta_com=PORTA_ESP32)
    camada2.iniciar_ligacao()
    time.sleep(2)  
    
    try:
        modulo_teste_desempenho(camada2, numero_tramas=100) 
    except KeyboardInterrupt:
        gerar_log("TESTE STRESS", "A avaliação foi interrompida manualmente pelo administrador.", "AVISO")
    finally:
        camada2.fechar_ligacao()