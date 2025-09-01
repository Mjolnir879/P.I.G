"""
Cliente de rede para comunicação com o servidor multiplayer
"""
import socketio
from typing import Callable, Dict, Any

class NetworkClient:
    """
    Cliente para comunicação com servidor multiplayer via Socket.IO
    Gerencia conexão, desconexão e troca de mensagens com o servidor
    """
    
    def __init__(self, server_url: str = "http://localhost:3000"):
        # URL do servidor ao qual se conectar
        self.server_url = server_url
        # Instância do cliente Socket.IO
        self.sio = socketio.Client()
        # Callbacks registrados para diferentes tipos de mensagem
        self.callbacks: Dict[str, Callable] = {}
        # Estado de conexão
        self.connected = False
        
        # Configura handlers padrão
        self.setup_default_handlers()
        
    def setup_default_handlers(self) -> None:
        """Configura os handlers padrão para eventos de conexão e desconexão"""
        
        @self.sio.event
        def connect():
            """Callback chamado quando conectado ao servidor"""
            print("Conectado ao servidor")
            self.connected = True
            
        @self.sio.event
        def disconnect():
            """Callback chamado quando desconectado do servidor"""
            print("Desconectado do servidor")
            self.connected = False
            
    def register_callback(self, event_name: str, callback: Callable) -> None:
        """
        Registra um callback para um tipo específico de mensagem
        O callback será chamado quando uma mensagem com este evento for recebida
        """
        self.callbacks[event_name] = callback
        
        # Registra o handler no Socket.IO
        @self.sio.on(event_name)
        def handler(data):
            callback(data)
            
    def connect(self) -> None:
        """Estabelece conexão com o servidor"""
        try:
            self.sio.connect(self.server_url)
        except Exception as e:
            print(f"Erro ao conectar com o servidor: {e}")
            
    def disconnect(self) -> None:
        """Desconecta do servidor"""
        self.sio.disconnect()
        
    def send(self, event_name: str, data: Any = None) -> None:
        """
        Envia uma mensagem para o servidor
        Só funciona se estiver conectado
        """
        if self.connected:
            self.sio.emit(event_name, data)
        else:
            print("Não conectado ao servidor. Não é possível enviar mensagem.")