import socket
import uuid
import os
import json
import getpass
from datetime import datetime, timezone
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
from mensagem import Mensagem
from cryptography.x509 import load_pem_x509_certificate, NameOID, CertificateBuilder
from cryptography import x509


class Client:
    def __init__(self, client_id, password, server_host="localhost", server_port=500):
        # Inicializa um cliente com ID, senha e endereço do servidor.
        self.client_id = client_id
        self.server_host = server_host
        self.server_port = server_port
        
        # Caminhos para a chave privada e o certificado do cliente.
        self.private_key_path = f"certs/client{self.client_id}_key.pem"
        self.certificate_path = f"certs/client{self.client_id}_cert.pem"
        
        # Password para proteger a chave privada.
        self.password = password.encode()
        
        # Carrega a chave privada e o certificado do cliente.
        self.private_key = self.load_private_key()
        self.client_cert = self.load_certificate()
        
        # Variável para armazenar a chave AES após troca segura.
        self.key = None

    # Função para carregar a chave privada do cliente.
    def load_private_key(self):
        try:
            with open(self.private_key_path, "rb") as key_file:
                return serialization.load_pem_private_key(key_file.read(), password=self.password)
        except FileNotFoundError:
            print(f"Error: Private key file '{self.private_key_path}' not found.")
            raise
        except ValueError:
            print("Error: Incorrect password for private key.")
            raise

    # Função para carregar o certificado do cliente.
    def load_certificate(self):
        try:
            with open(self.certificate_path, "rb") as cert_file:
                return cert_file.read()
        except FileNotFoundError:
            print(f"Error: Certificate file '{self.certificate_path}' not found.")
            raise
    
    # Função para gerar um id aleatório para o campo id_msg
    def gerar_id_msg(self):
        return str(uuid.uuid4())

    # Função para verificar a validade do certificado do servidor.
    def validate_server_certificate(self, cert_bytes):
        try:
            server_cert = load_pem_x509_certificate(cert_bytes)
            current_time = datetime.now(timezone.utc)

            if current_time < server_cert.not_valid_before_utc:
                print("Certificate is not yet valid.")
                return None

            if current_time > server_cert.not_valid_after_utc:
                print("Certificate has expired.")
                return None

            return server_cert

        except Exception as e:
            print(f"Invalid server certificate: {e}")
            return None
    
    #Função para um cliente se conectar
    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        
        # Envia-se o certificado do cliente pelo socket do cliente.
        self.client_socket.send(self.client_cert)
        print("Client certificate sent.")
        
        # O socket do cliente recebe o certificado do servidor e verifica se é válido.
        server_cert_bytes = self.client_socket.recv(2048)
        server_cert = self.validate_server_certificate(server_cert_bytes)
        if not server_cert:
            print("Closing connection due to invalid server certificate.")
            self.client_socket.close()
            return
        print("Server certificate validated.")
        
        # Gera-se a chave publica para um cliente a partir da sua chave privada RSA.
        public_key = self.private_key.public_key()
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Envia-se pelo o socket do cliente a chave publica.
        self.client_socket.send(public_key_bytes)
        print("Public key sent.")

        # O socket do cliente recebe a chave encriptada AES e usa a chave privada do cliente para a decifrar.
        encrypted_key = self.client_socket.recv(256)
        self.key = self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("AES key received and decrypted.\n")
        
    
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

    # Função usada para assinar uma mensagem. Usamos a chave privada para assinar.
    def sign_message(self, message):
        return self.private_key.sign(
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

    # Função associada á ação para enviar uma mensagem.
    def send_message(self, id_msg, id_destinatario, assunto="Sem Assunto", conteudo=""):
        self.connect()

        timestamp = datetime.now().isoformat()

        mensagem = Mensagem(id_msg, self.client_id, id_destinatario, assunto, conteudo, timestamp)

        json_message = mensagem.to_json()
        
        # O cliente assina a mensagem.
        signature = self.sign_message(json_message.encode("utf-8"))
        
        public_key = self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode("utf-8")
        
        # É enviada a mensagem em formato JSON. Enviamos a mensagem, a assinatura e a chave pública.
        data_to_send = {
            "action": "send_message",
            "message": json_message,
            "signature": signature.hex(),
            "public_key": public_key
        }
        
        # Antes de enviar a solicitação o cliente encripta os dados com AES.
        encrypted_data = self.encrypt_message(json.dumps(data_to_send))
        self.client_socket.send(encrypted_data)
        
        # O cliente recebe uma resposta do servidor.
        encrypted_response = self.client_socket.recv(1024)
        
        # A resposta do servidor é desencriptada ao usar a chave AES previamente compartilhada com o servidor.
        decrypted_response = self.decrypt_message(encrypted_response)
        response_data = json.loads(decrypted_response)

        if response_data.get("status") == "success":
            print(f"Server Response: {response_data.get('message')}")
        else:
            print(f"Error: {response_data.get('error')}")

        self.client_socket.close()
    
    # Função usada para o cliente consultar as mensagens
    def request_messages(self):
        self.connect()

        request_data = {
            "action": "get_messages",
            "recipient_id": self.client_id
        }
        
        # Antes de enviar a solicitação o cliente encripta os dados com AES.
        encrypted_request = self.encrypt_message(json.dumps(request_data))
        self.client_socket.send(encrypted_request)

        # O cliente recebe uma resposta do servidor.
        encrypted_response = self.client_socket.recv(4096)
        
        # A resposta do servidor é desencriptada ao usar a chave AES previamente compartilhada com o servidor.
        decrypted_response = self.decrypt_message(encrypted_response)
        response_data = json.loads(decrypted_response)
        
        if response_data.get("status") == "success":
            messages = response_data.get("messages", [])
            for msg in messages:
                message_data = msg['message']
                signature = bytes.fromhex(msg['signature'])
                public_key_pem = msg['public_key']
                
                # A chave publica do cliente remetente é carregada para validar a assinatura.
                public_key = serialization.load_pem_public_key(
                    public_key_pem.encode("utf-8")
                )
                
                # O cliente usa a chave pública do cliente remetente para valida a assinatura.
                public_key.verify(
                    signature,
                    message_data.encode("utf-8"),
                    padding.PKCS1v15(),
                    hashes.SHA256()
                )
                
                # Mostra a mensagem enviada por outro cliente.
                mensagem = Mensagem.from_json(message_data)
                print(f"\n--- Message from {mensagem.id_origem} ---")
                print(f"ID: {mensagem.id_msg}")
                print(f"To: {mensagem.id_destinatario}")
                print(f"Subject: {mensagem.assunto}")
                print(f"Content: {mensagem.conteudo}")
                print(f"Timestamp: {mensagem.timestamp}\n")
        else:
            print(f"Error: {response_data.get('error')}")

        self.client_socket.close()
        
    # Função relativa á ação para consultar novas mensagens.
    def request_new_messages(self):
        self.connect()

        request_data = {
            "action": "get_new_messages",
            "recipient_id": self.client_id
        }
        
        # Antes de enviar a solicitação o cliente encripta os dados com AES.
        encrypted_request = self.encrypt_message(json.dumps(request_data))
        self.client_socket.send(encrypted_request)
        
        # O cliente recebe uma resposta do servidor.
        encrypted_response = self.client_socket.recv(4096)
        
        # A resposta do servidor é desencriptada ao usar a chave AEs previamente compartilhada com o servidor.
        decrypted_response = self.decrypt_message(encrypted_response)
        response_data = json.loads(decrypted_response)
        
        if response_data.get("status") == "success":
            messages = response_data.get("messages", [])
            for msg in messages:
                message_data = msg['message']
                signature = bytes.fromhex(msg['signature'])
                public_key_pem = msg['public_key']
                
                # A chave publica do cliente remetente é carregada para validar a assinatura.
                public_key = serialization.load_pem_public_key(
                    public_key_pem.encode("utf-8")
                )
                
                # O cliente usa a chave pública do cliente remetente para valida a assinatura.
                public_key.verify(
                    signature,
                    message_data.encode("utf-8"),
                    padding.PKCS1v15(),
                    hashes.SHA256()
                )
                
                # Mostra a mensagem enviada por outro cliente.
                mensagem = Mensagem.from_json(message_data)
                print(f"\n--- New Message from {mensagem.id_origem} ---")
                print(f"ID: {mensagem.id_msg}")
                print(f"To: {mensagem.id_destinatario}")
                print(f"Subject: {mensagem.assunto}")
                print(f"Content: {mensagem.conteudo}")
                print(f"Timestamp: {mensagem.timestamp}\n")
                
                # Marca a mensagem como lida através do id da mensagem.
                self.mark_message_as_read(mensagem.id_msg)
            
            else:
                print(f"Error: {response_data.get('error')}")

        self.client_socket.close()
    
    # Função relativa á ação para marcar uma mensagem como lida.
    def mark_message_as_read(self, id_msg):
        self.connect()

        mark_as_read_data = {
            "action": "mark_as_read",
            "recipient_id": self.client_id,
            "id_msg": id_msg
        }
        
        # Antes de enviar a solicitação o cliente encripta os dados com AES.
        encrypted_request = self.encrypt_message(json.dumps(mark_as_read_data))
        self.client_socket.send(encrypted_request)
        
        # O cliente recebe uma resposta do servidor.
        encrypted_response = self.client_socket.recv(1024)
        
        # A resposta do servidor é desencriptada ao usar a chave AEs previamente compartilhada com o servidor.
        decrypted_response = self.decrypt_message(encrypted_response)
        response_data = json.loads(decrypted_response)

        if response_data.get("status") == "success":
            print(f"Server Response: {response_data.get('message')}")
        else:
            print(f"Error: {response_data.get('error')}")

        self.client_socket.close()

    # Função relativa á ação para eliminar uma mensagem.
    def delete_message(self, id_msg):
        self.connect()

        delete_data = {
            "action": "delete_message",
            "recipient_id": self.client_id,
            "id_msg": id_msg
        }

        # Antes de enviar a solicitação o cliente encripta os dados com AES.
        encrypted_request = self.encrypt_message(json.dumps(delete_data))
        self.client_socket.send(encrypted_request)

        # O cliente recebe uma resposta do servidor.
        encrypted_response = self.client_socket.recv(1024)
        
        # A resposta do servidor é desencriptada ao usar a chave AEs previamente compartilhada com o servidor.
        decrypted_response = self.decrypt_message(encrypted_response)
        response_data = json.loads(decrypted_response)

        if response_data.get("status") == "success":
            print(f"Server Response: {response_data.get('message')}")
        else:
            print(f"Error: {response_data.get('error')}")

        self.client_socket.close()
    
    
    # Função relativa á ação para consultar uma mensagem especifica.
    def request_specific_message(self, id_msg):
        self.connect()

        request_data = {
            "action": "get_specific_message",
            "recipient_id": self.client_id,
            "id_msg": id_msg
        }
        
        # Antes de enviar a solicitação o cliente encripta os dados com AES.
        encrypted_request = self.encrypt_message(json.dumps(request_data))
        self.client_socket.send(encrypted_request)

        # O cliente recebe uma resposta do servidor.
        encrypted_response = self.client_socket.recv(4096)
        
        # A resposta do servidor é desencriptada ao usar a chave AEs previamente compartilhada com o servidor.
        decrypted_response = self.decrypt_message(encrypted_response)
        response_data = json.loads(decrypted_response)

        if response_data.get("status") == "success":
            message_data = response_data.get("message")
            signature = bytes.fromhex(response_data.get("signature"))
            public_key_pem = response_data.get("public_key")
            
            # A chave publica do cliente remetente é carregada para validar a assinatura.
            public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
            
            # Valida a assinatura presente na mensagem com a chave pública do cliente remetente.
            public_key.verify(
                signature,
                message_data.encode("utf-8"),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            
            # Mostra a mensagem enviada por outro cliente.
            mensagem = Mensagem.from_json(message_data)
            print(f"\n--- New Message from {mensagem.id_origem} ---")
            print(f"ID: {mensagem.id_msg}")
            print(f"To: {mensagem.id_destinatario}")
            print(f"Subject: {mensagem.assunto}")
            print(f"Content: {mensagem.conteudo}")
            print(f"Timestamp: {mensagem.timestamp}\n")
        else:
            print(f"Error: {response_data.get('error')}")

        self.client_socket.close()

    # Menu para o cliente poder realizar uma ação.
    def show_menu(self):
        while True:
            print("\n===== Menu =====")
            print("1. Send a message")
            print("2. Read all messages")
            print("3. Read new messages")
            print("4. Read a specific message")
            print("5. Delete a message ")
            print("6. Exit")

            choice = input("Choose an option: ")
            print("")

            if choice == "1":
                id_destinatario = input("Enter the recipient ID: ")
                assunto = input("Enter the subject: ")
                conteudo = input("Enter the content: ")
                print("")
                id_msg = self.gerar_id_msg()
                self.send_message(id_msg, id_destinatario, assunto, conteudo)

            elif choice == "2":
                self.request_messages()
                print("")

            elif choice == "3":
                self.request_new_messages()
                print("")

            elif choice == "4":
                id_msg = input("Enter the ID of the message to read: ")
                print("")
                self.request_specific_message(id_msg)

            elif choice == "5":
                id_msg = input("Enter the ID of the message to delete: ")
                print("")
                self.delete_message(id_msg)

            elif choice == "6":
                print("Exiting...")
                break

            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    client_id = input("Enter your client ID: ")
    password = getpass.getpass("Enter your password: ")
    client = Client(client_id, password)
    client.show_menu()
