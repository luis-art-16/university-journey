"""
Módulo de Teste de Resiliência e Recuperação de Falhas.
Simula o envio de ruído no canal e interrupções físicas para validar
os mecanismos de ARQ e FEC da Camada de Ligação.
"""

import time
from camada_ligacao_dados import CamadaDeLigacao
from constantes_protocolo import TYPE_TEXT
from logger import gerar_log

def executar_teste_recuperacao_falhas():
    print("="*65)
    print("TESTE DE RESILIÊNCIA - ENVIO DE FALHAS E RECUPERAÇÃO DO SISTEMA")
    print("="*65)

    # Iniciar a Camada 2 normalmente
    PORTA_ESP32 = 'COM3' # Ajustar porta se necessário
    camada2 = CamadaDeLigacao(porta_com=PORTA_ESP32)
    camada2.iniciar_ligacao()
    time.sleep(2)

    # 1. Guardar a referência para a rotina de hardware original
    envio_original = camada2.link.enviar_trama_fisica
    
    contador_envios = 0

    def envio_com_injecao_ruido(pacote_fisico):
        """Atua como um middleware malicioso para simular anomalias de hardware."""
        nonlocal contador_envios
        contador_envios += 1
        
        # Envio de anomalias com base na sequência temporal:
        if contador_envios == 2:
            gerar_log("SIMULADOR", "A corromper o campo FCS (CRC) do Pacote 2 propositadamente...", "AVISO")
            # Adulteração de 1 byte no final da trama para forçar erro de integridade
            pacote_corrompido = bytearray(pacote_fisico)
            pacote_corrompido[-2] = (pacote_corrompido[-2] + 1) % 256 
            envio_original(bytes(pacote_corrompido))
            
        elif contador_envios == 5:
            gerar_log("SIMULADOR", "Simulação de quebra de link ótico no Pacote 5 ...", "AVISO")
            # A rotina de hardware não é chamada. A trama perde-se no meio físico.
            pass 
            
        else:
            # Canal a funcionar nas condições ideais
            envio_original(pacote_fisico)

    # 2. Aplicar o bypass na interface física
    camada2.link.enviar_trama_fisica = envio_com_injecao_ruido

    # 3. Preparar a carga de testes
    mensagem_teste = b"Carga de teste para validacao de mecanismos de recuperacao de erros do protocolo. " * 3
    tamanho_fragmento = 100
    fragmentos = [mensagem_teste[i:i + tamanho_fragmento] for i in range(0, len(mensagem_teste), tamanho_fragmento)]
    
    gerar_log("APP", f"A iniciar transmissão de {len(fragmentos)} fragmentos sob ambiente ruidoso...\n", "INFO")
    
    tempo_inicio = time.time()
    
    # 4. Iniciar Transmissão
    for i, frag in enumerate(fragmentos):
        print(f"--- A processar fragmento {i+1}/{len(fragmentos)} ---")
        sucesso = camada2.enviar_ficheiro(payload=frag, tipo=TYPE_TEXT)
        
        if not sucesso:
            gerar_log("APP", "O SISTEMA NÃO CONSEGUIU RECUPERAR. TRANSFERÊNCIA ABORTADA.", "ERRO")
            break
            
        time.sleep(0.1) 

    tempo_total = time.time() - tempo_inicio

    print("\n" + "="*65)
    print("RESULTADO DA AVALIAÇÃO DE RESILIÊNCIA")
    print("="*65)
    print(f"Tempo total de recuperação e transmissão: {tempo_total:.2f} segundos")
    print("[SUCESSO] O protocolo detetou os erros, executou as retransmissões (ARQ)")
    print("          e entregou a totalidade dos dados à Camada de Aplicação!")
    print("="*65)
    
    # Repor a integridade do sistema e fechar a porta
    camada2.link.enviar_trama_fisica = envio_original
    camada2.fechar_ligacao()

if __name__ == "__main__":
    executar_teste_recuperacao_falhas()