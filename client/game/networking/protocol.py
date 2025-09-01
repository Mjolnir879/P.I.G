"""
Protocolo de comunicação - define como as mensagens são serializadas e desserializadas
"""
import json
from .messages import *

class NetworkProtocol:
    """
    Define o protocolo de comunicação entre cliente e servidor
    Responsável por serializar e desserializar mensagens
    """
    
    @staticmethod
    def serialize_message(message: Any) -> str:
        """
        Serializa uma mensagem para envio pela rede
        message: Instância de uma mensagem (dataclass)
        Retorna a mensagem serializada como string JSON
        """
        # Adiciona um campo type para identificar o tipo de mensagem
        message_dict = {
            'type': message.__class__.__name__,
            'data': message.__dict__
        }
        return json.dumps(message_dict)
        
    @staticmethod
    def deserialize_message(message_str: str) -> Any:
        """
        Desserializa uma mensagem recebida da rede
        message_str: Mensagem serializada como string JSON
        Retorna a mensagem desserializada (instância da dataclass apropriada)
        """
        message_dict = json.loads(message_str)
        message_type = message_dict['type']
        message_data = message_dict['data']
        
        # Mapeia nomes de tipos para classes de mensagem
        message_classes = {
            'PlayerJoinMessage': PlayerJoinMessage,
            'PlayerLeaveMessage': PlayerLeaveMessage,
            'PlayerInputMessage': PlayerInputMessage,
            'PlayerActionMessage': PlayerActionMessage,
            'GameStateUpdateMessage': GameStateUpdateMessage,
            'EntityCreateMessage': EntityCreateMessage,
            'EntityDestroyMessage': EntityDestroyMessage
        }
        
        if message_type in message_classes:
            return message_classes[message_type](**message_data)
        else:
            raise ValueError(f"Tipo de mensagem desconhecido: {message_type}")