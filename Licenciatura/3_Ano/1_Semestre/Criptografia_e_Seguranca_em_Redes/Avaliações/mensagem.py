import json
from datetime import datetime

class Mensagem:
    def __init__(self, id_msg, id_origem, id_destinatario, assunto, conteudo, timestamp):
        # Campos que uma mensagem contêm.
        self.id_msg = id_msg
        self.id_origem = id_origem
        self.id_destinatario = id_destinatario
        self.assunto = assunto[:50]
        self.conteudo = conteudo
        self.timestamp = timestamp 
        
    # Passa os dados em plaintext para JSON.
    def to_json(self):
        return json.dumps({
            "id_msg": self.id_msg,
            "id_origem": self.id_origem,
            "id_destinatario": self.id_destinatario,
            "assunto": self.assunto,
            "conteudo": self.conteudo,
            "timestamp": self.timestamp
        })

    @staticmethod
    # Passa os dados de JSON para plaintext.
    def from_json(json_string):
        data = json.loads(json_string)
        return Mensagem(
            id_msg=data['id_msg'],
            id_origem=data['id_origem'],
            id_destinatario=data['id_destinatario'],
            assunto=data['assunto'],
            conteudo=data['conteudo'],
            timestamp=data['timestamp']
        )

