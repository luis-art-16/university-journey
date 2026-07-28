from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import NameOID
from cryptography import x509
from datetime import datetime, timedelta
import os

#Gerar as chaves privadas dos clientes e do servidor ao usar RSA
def generate_key():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return key

#Gerar os certificados do servidor e do cliente.
def generate_certificate(subject_name, issuer_name, key, issuer_key):
    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, subject_name),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "UM"),
        x509.NameAttribute(NameOID.COUNTRY_NAME, "PT"),
    ])
    issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, issuer_name),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "UM"),
        x509.NameAttribute(NameOID.COUNTRY_NAME, "PT"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]),
        critical=False
    ).sign(issuer_key, hashes.SHA256())

    return cert

# Para guardar as chaves privadas e os certificados em ficheiros PEM. Estes ficheiros são encriptados com uma password associada a cada um deles.
def save_key_and_cert(key, cert, key_filename, cert_filename, password):
    with open(key_filename, "wb") as key_file:
        key_file.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
        ))

    with open(cert_filename, "wb") as cert_file:
        cert_file.write(cert.public_bytes(serialization.Encoding.PEM))

if __name__ == "__main__":
    # Para fazer uma diretoria onde serão guardados os certificados e as chaves privadas.
    os.makedirs("certs", exist_ok=True)

    server_key = generate_key()
    server_cert = generate_certificate("Server", "Server", server_key, server_key)
    save_key_and_cert(server_key, server_cert, "certs/server_key.pem", "certs/server_cert.pem", "server_secure_password")

    # Dicionário relativo ás passwords de cada cliente.
    client_passwords = {
        "clientA": "passwordA",
        "clientB": "passwordB",
        "clientC": "passwordC",
        "clientD": "passwordD",
        "clientE": "passwordE",
    }
    
    for client_id, password in client_passwords.items():
        client_key = generate_key()
        client_cert = generate_certificate(client_id, "Server", client_key, server_key)
        save_key_and_cert(client_key, client_cert, f"certs/{client_id}_key.pem", f"certs/{client_id}_cert.pem", password)

    print("Certificates and keys successfully generated in 'certs/'")
