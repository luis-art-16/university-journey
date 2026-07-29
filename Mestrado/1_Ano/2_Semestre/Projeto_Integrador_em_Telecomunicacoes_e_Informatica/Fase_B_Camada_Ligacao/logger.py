import datetime

def gerar_log(modulo, mensagem, tipo="INFO"):
    """Tipos: INFO (Azul), SUCESSO (Verde), AVISO (Amarelo), ERRO (Vermelho)"""
    hora = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    cores = {
        "INFO": "\033[94m",     
        "SUCESSO": "\033[92m",  
        "AVISO": "\033[93m",    
        "ERRO": "\033[91m",     
        "RESET": "\033[0m"
    }
    cor = cores.get(tipo, cores["RESET"])
    print(f"{cor}[{hora}] [{modulo}] {mensagem}{cores['RESET']}")