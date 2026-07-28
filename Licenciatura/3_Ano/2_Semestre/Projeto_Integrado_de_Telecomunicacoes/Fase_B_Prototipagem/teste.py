import socket

def testar_conexao(ip, porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)  # tempo limite de 3 segundos

    try:
        sock.connect((ip, porta))
        print(f"✅ Conexão bem-sucedida com {ip}:{porta}")
    except socket.error as e:
        print(f"❌ Não foi possível conectar em {ip}:{porta}")
        print(f"Erro: {e}")
    finally:
        sock.close()

# Testar localhost na porta MQTT padrão
testar_conexao("127.0.0.1", 1883)


