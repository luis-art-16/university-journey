"""
Aplicação Servidor (Recetor).
Mantém a escuta ativa e contínua no canal de comunicações, processando
e armazenando localmente os ficheiros reconstruídos pela Camada de Ligação.
"""
import time
from camada_ligacao_dados import CamadaDeLigacao
from logger import gerar_log

def iniciar_servidor(): ##ciclo infinito
    """
    Inicia o serviço de receção contínua e gere os mecanismos de 
    recuperação de estado da aplicação.
    """
    PORTA_COM = 'COM3' # Interface série ligada à ESP32 que irá receber os dados
    camada2 = CamadaDeLigacao(porta_com=PORTA_COM)
    camada2.iniciar_ligacao()
    time.sleep(2) # Tempo de estabilização do hardware
    
    camada2.buffer_rececao.clear()
    
    gerar_log("SERVIDOR", "Serviço iniciado com sucesso.", "SUCESSO")
    gerar_log("SERVIDOR", "À escuta no canal físico. A aguardar tráfego...", "INFO")
    
    try:
        while True:
            # Entrega o controlo à Camada 2 para processamento de tramas na fila
            camada2._escutar_canal_arq()                                              ##
            
            # ==========================================
            # MONITOR DE INATIVIDADE (TIMEOUT DE SESSÃO)
            # ==========================================
            # Verifica se existem dados parciais no buffer (Sessão pendente)
            # E o emissor está em silêncio há mais de 10s...
            if len(camada2.buffer_rececao) > 0:
                tempo_silencio = time.time() - camada2.ultimo_tempo_rececao
                
                if tempo_silencio > 10.0:
                    gerar_log("TIMEOUT", "Tempo limite excedido. A ligação parece ter caído.", "ERRO")
                    gerar_log("TIMEOUT", "A limpar buffer e a repor sincronismo da máquina de estados.", "AVISO")
                    
                    # Flush ao buffer e preparar a máquina de estados para a próxima tentativa
                    camada2.buffer_rececao.clear()
                    camada2.arq.seq_num_esperado = 0
                    
                    # Atualização do relógio interno para evitar ciclo infinito de alertas
                    camada2.ultimo_tempo_rececao = time.time()
                    gerar_log("TIMEOUT", "Sistema estabilizado. A aguardar nova transferência.", "INFO")
                    
            time.sleep(0.01) # Evitar uso excessivo de CPU no ciclo de escuta
            
    except KeyboardInterrupt:
        gerar_log("SERVIDOR", "Servidor encerrado pelo utilizador (Ctrl+C).", "AVISO")
    finally:
        camada2.fechar_ligacao()

if __name__ == "__main__":
    iniciar_servidor()