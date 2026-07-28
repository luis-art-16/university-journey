import socket
import os
import json
from datetime import datetime, timezone
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
from mensagem import Mensagem
from cryptography.x509 import load_pem_x509_certificate, NameOID, CertificateBuilder
from cryptography import x509


class Server:
    def __init__(self, host="192.168.137.147", port=500):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # O servidor escuta até 5 conexões simultâneas.
        print(f"Server running on {self.host}:{self.port}\n")
        
        # Carrega o certificado do servidor em formato PEM.
        with open("certs/server_cert.pem", "rb") as cert_file:  
            self.server_cert = load_pem_x509_certificate(cert_file.read()) 
        
        # Dicionário para armazenar mensagens recebidas.
        self.messages = {}  
        
        # Dicionário para mensagens novas destinadas a clientes.
        self.new_messages = {}
    
    # Função para verificar se o certificado do cliente é válido.
    def validate_client_certificate(self, cert_bytes):
        try:
            client_cert = load_pem_x509_certificate(cert_bytes) # Carrega o certificado do cliente em formato PEM.
            current_time = datetime.now(timezone.utc)  

            # Verifica se o certificado é válido (não expirou e está dentro do período de validade).
            if current_time < client_cert.not_valid_before_utc:
                print("Certificate is not yet valid.")  
                return None

            if current_time > client_cert.not_valid_after_utc:
                print("Certificate has expired.") 
                return None

            return client_cert 

        except Exception as e:
            print(f"Invalid server certificate: {e}")  
            return None

    # Função usada para encriptar uma mensagem ao usar o AES no modo CBC.
    def encrypt_message(self, plaintext):
        iv = os.urandom(16) 
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor() 
        padded_plaintext = plaintext + ' ' * (16 - len(plaintext) % 16)  
        encrypted_data = encryptor.update(padded_plaintext.encode()) + encryptor.finalize()
        return iv + encrypted_data  

    # Função usada para desencriptar uma mensagem ao usar o AES no modo CBC.
    def decrypt_message(self, encrypted_message):
        iv = encrypted_message[:16]  
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())  
        decryptor = cipher.decryptor() 
        decrypted_data = decryptor.update(encrypted_message[16:]) + decryptor.finalize() 
        return decrypted_data.decode().strip()  

    def handle_client(self, client_socket, addr):
     try: 
        print(f"\nConnection accepted from: {addr}\n")  
        
        # Recebe o certificado do cliente.
        client_cert_bytes = client_socket.recv(2048) 
        
        # Valida o certificado do cliente.
        client_cert = self.validate_client_certificate(client_cert_bytes) 
        if not client_cert:  # Se o certificado for inválido:
            print("Closing connection due to invalid certificate.")  # Exibe mensagem de erro.
            client_socket.close()  # Fecha a conexão.
            return
        print("Client certificate validated.")  # Certificado válido.

        # Envia o certificado do servidor para o cliente.
        client_socket.send(self.server_cert.public_bytes(serialization.Encoding.PEM))
        print("Server certificate sent.")  

        # Recebe a chave pública do cliente.
        public_key_bytes = client_socket.recv(4096)
        print("Public Key Received") 
        
        # Carrega a chave pública do cliente a partir do formato PEM.
        client_public_key = serialization.load_pem_public_key(
            public_key_bytes,
            backend=default_backend()
        ) 

        # Gera uma chave AES aleatória de 32 bytes.
        self.key = os.urandom(32)
        encrypted_aes_key = client_public_key.encrypt(
            self.key,  # Encripta a chave AES usando a chave pública do cliente.
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),  
                algorithm=hashes.SHA256(), 
                label=None
            )
        )
        
        # Envia a chave AES encriptada para o cliente.
        client_socket.send(encrypted_aes_key)  
        print("AES key sent.")  

        # Recebe dados encriptados do cliente.
        encrypted_data = client_socket.recv(4096)  
        
        # Desencripta os dados usando a chave AES.
        decrypted_data = self.decrypt_message(encrypted_data)  
        data = json.loads(decrypted_data)  
        
        action = data.get("action")

        if action == "get_messages":
            # Recupera todas as mensagens associadas ao destinatário, marca como não novas, e as envia encriptadas.
            recipient_id = data["recipient_id"]
            messages = self.messages.get(recipient_id, [])

            for msg in messages:
                msg["is_new"] = False

            response = {
                "status": "success",
                "messages": messages
            }
            encrypted_response = self.encrypt_message(json.dumps(response))
            client_socket.send(encrypted_response)


        elif action == "get_new_messages":
            # Recupera apenas as mensagens novas para o destinatário e marca como não novas.
            recipient_id = data["recipient_id"]
            messages = self.messages.get(recipient_id, [])
            new_messages = [msg for msg in messages if msg["is_new"]]
          
            for new_msg in new_messages:
                new_msg["is_new"] = False

            if new_messages:
                if recipient_id not in self.messages:
                    self.messages[recipient_id] = []
                for new_msg in new_messages:
                    if new_msg not in self.messages[recipient_id]:
                        self.messages[recipient_id].append(new_msg)

                self.new_messages[recipient_id] = []
            
            response = {
                "status": "success",
                "messages": new_messages
            }
            
            encrypted_response = self.encrypt_message(json.dumps(response))
            client_socket.send(encrypted_response)


        elif action == "send_message":
            # Adiciona uma nova mensagem ao destinatário especificado, incluindo assinatura e chave pública do remetente.
            message_data = data['message']
            signature = data['signature']
            public_key = data['public_key']

            mensagem = Mensagem.from_json(message_data)
            destinatario = mensagem.id_destinatario

            if destinatario not in self.messages:
                self.messages[destinatario] = []

            self.messages[destinatario].append({
                "id_msg": mensagem.id_msg,
                "message": message_data,
                "signature": signature,
                "public_key": public_key,
                "is_new": True
            })

            response = {
                "status": "success",
                "message": f"Message stored for recipient: {destinatario}"
            }
            encrypted_response = self.encrypt_message(json.dumps(response))
            client_socket.send(encrypted_response)


        elif action == "delete_message":
            # Remove uma mensagem específica do destinatário, se existir.
            recipient_id = data["recipient_id"]
            id_msg = data["id_msg"]
            recipient_messages = self.messages.get(recipient_id, [])

            message_found = False
            for msg in recipient_messages:
                if msg["id_msg"] == id_msg:
                    recipient_messages.remove(msg)
                    message_found = True
                    response = {
                        "status": "success",
                        "message": f"Message {id_msg} deleted successfully."
                    }
                    break

            if not message_found:
                response = {
                    "status": "error",
                    "error": f"Message {id_msg} not found for recipient {recipient_id}."
                }

            encrypted_response = self.encrypt_message(json.dumps(response))
            client_socket.send(encrypted_response)


        elif action == "mark_as_read":
            # Marca uma mensagem específica como lida (não nova) para o destinatário.
            recipient_id = data["recipient_id"]
            id_msg = data["id_msg"]
            recipient_messages = self.messages.get(recipient_id, [])

            for msg in recipient_messages:
                if msg["id_msg"] == id_msg:
                    msg["is_new"] = False
                    
                    if recipient_id in self.new_messages:
                        self.new_messages[recipient_id] = [
                            new_msg for new_msg in self.new_messages[recipient_id] if new_msg["id_msg"] != id_msg
                        ]

                    response = {
                        "status": "success",
                        "message": f"Message {id_msg} marked as read."
                    }
                    break
            else:
                response = {
                    "status": "error",
                    "error": f"Message {id_msg} not found for recipient {recipient_id}."
                }

            encrypted_response = self.encrypt_message(json.dumps(response))
            client_socket.send(encrypted_response)


        elif action == "get_specific_message":
            # Recupera uma mensagem específica pelo ID, se existir.
            recipient_id = data["recipient_id"]
            id_msg = data["id_msg"]

            messages = self.messages.get(recipient_id, [])
            specific_message = next((msg for msg in messages if msg["id_msg"] == id_msg), None)

            if specific_message:
                response = {
                    "status": "success",
                    "message": specific_message["message"],
                    "signature": specific_message["signature"],
                    "public_key": specific_message["public_key"]
                }
            else:
                response = {
                    "status": "error",
                    "error": f"Message with ID {id_msg} not found."
                }

            encrypted_response = self.encrypt_message(json.dumps(response))
            client_socket.send(encrypted_response)


     finally:
        client_socket.close()


    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.handle_client(client_socket, addr)

if __name__ == "__main__":
    server = Server()
    server.start()

