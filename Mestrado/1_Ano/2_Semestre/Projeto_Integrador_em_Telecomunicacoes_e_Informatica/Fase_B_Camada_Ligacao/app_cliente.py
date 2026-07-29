"""
Aplicação Cliente (Emissor).
Responsável por ler ficheiros do sistema de ficheiros local, determinar o seu tipo,
e entregar a transferência à Camada de Ligação de Dados.
"""
import time
import os
import sys
from camada_ligacao_dados import CamadaDeLigacao
from constantes_protocolo import TYPE_TEXT, TYPE_IMAGE, TYPE_EOF
from logger import gerar_log 

def enviar_ficheiro_aplicacao(caminho_ficheiro: str, tipo_ficheiro: int): ##
    """
    Inicia o processo de transferência de um ficheiro para o servidor.
    """
    PORTA_COM = 'COM3' # Interface série ligada à ESP32 que irá transmitir os dados
    camada2 = CamadaDeLigacao(porta_com=PORTA_COM)
    camada2.iniciar_ligacao()
    time.sleep(2) # Tempo de estabilização do hardware
    
    # 1. Validação de existência do ficheiro
    if not os.path.exists(caminho_ficheiro):
        gerar_log("CLIENTE", f"Erro: O ficheiro '{caminho_ficheiro}' não foi encontrado no diretorio.", "ERRO")
        camada2.fechar_ligacao()
        return

    # 2. Leitura dos dados em modo binário
    with open(caminho_ficheiro, 'rb') as f:
        dados_completos = f.read()

    gerar_log("CLIENTE", f"Ficheiro '{caminho_ficheiro}' carregado na memória ({len(dados_completos)} bytes).", "INFO")
    
    # 3. Fragmentação dos dados à camada de aplicação
    tamanho_fragmento = 100
    fragmentos = [dados_completos[i:i + tamanho_fragmento] for i in range(0, len(dados_completos), tamanho_fragmento)]
    
    tempo_inicio = time.time()
    sucesso_total = True
    
    # 4. Transmissão sequencial
    for i, frag in enumerate(fragmentos):
        gerar_log("CLIENTE", f"A transmitir fragmento {i+1}/{len(fragmentos)}...", "INFO")
        
        sucesso = camada2.enviar_ficheiro(payload=frag, tipo=tipo_ficheiro)
        
        if not sucesso:
            gerar_log("CLIENTE", f"Falha na entrega do fragmento {i+1}. Transferência abortada.", "ERRO")
            sucesso_total = False
            break
            
        time.sleep(0.01) # Pausa para não sobrecarregar o CPU
    
    tempo_total = time.time() - tempo_inicio
    
    # 5. Encerramento da Sessão (Envio de EOF)
    if sucesso_total:
        _, extensao = os.path.splitext(caminho_ficheiro)
        if not extensao: 
            extensao = ".bin" 
            
        gerar_log("CLIENTE", f"Sessão terminada. A transmitir flag EOF (Extensão: '{extensao}')...", "INFO")
        camada2.enviar_ficheiro(payload=extensao.encode('utf-8'), tipo=TYPE_EOF) ##
        
        gerar_log("CLIENTE", f"Transferência concluída com sucesso em {tempo_total:.2f} segundos.", "SUCESSO")  ##
    else:
        gerar_log("CLIENTE", "A transferência não pôde ser concluída.", "ERRO")
        
    camada2.fechar_ligacao()

if __name__ == "__main__":
    # Processamento de argumentos da linha de comandos
    if len(sys.argv) < 2:
        print("Uso incorreto da aplicação.")
        print("Sintaxe: python app_cliente.py <caminho_para_o_ficheiro>")
        sys.exit(1) 

    ficheiro_alvo = sys.argv[1]
    
    # Classificação de tráfego
    extensoes_imagem = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    if ficheiro_alvo.lower().endswith(extensoes_imagem):
        tipo_inferido = TYPE_IMAGE
        gerar_log("SISTEMA", "Classificação de tráfego: Multimédia (IMAGEM)", "INFO")
    else:
        tipo_inferido = TYPE_TEXT
        gerar_log("SISTEMA", "Classificação de tráfego: Documento (TEXTO/BINÁRIO)", "INFO")
        
    enviar_ficheiro_aplicacao(ficheiro_alvo, tipo_inferido)