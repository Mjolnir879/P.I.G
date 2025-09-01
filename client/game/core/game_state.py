"""
Gerenciador de estado do jogo - mantém e sincroniza o estado global do jogo
"""
from typing import Dict, Any, Set

class GameState:
    """
    Mantém o estado global do jogo e fornece métodos para acessá-lo e modificá-lo
    Atua como uma única fonte de verdade para o estado do jogo
    """
    
    def __init__(self):
        # Estado global do jogo
        self.state: Dict[str, Any] = {}
        # Listeners para mudanças de estado
        self.listeners: Dict[str, Set[Callable]] = {}
        
    def set(self, key: str, value: Any, notify: bool = True) -> None:
        """
        Define um valor no estado global
        Se notify for True, notifica todos os listeners registrados para esta chave
        """
        old_value = self.state.get(key)
        self.state[key] = value
        
        # Notifica listeners se o valor mudou e notify é True
        if notify and key in self.listeners and old_value != value:
            for callback in self.listeners[key]:
                callback(value, old_value)
                
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém um valor do estado global
        Retorna o valor padrão se a chave não existir
        """
        return self.state.get(key, default)
        
    def subscribe(self, key: str, callback: Callable) -> None:
        """
        Registra um callback para ser notificado quando um valor específico mudar
        O callback recebe (new_value, old_value) como argumentos
        """
        if key not in self.listeners:
            self.listeners[key] = set()
        self.listeners[key].add(callback)
        
    def unsubscribe(self, key: str, callback: Callable) -> None:
        """
        Remove um callback previamente registrado para uma chave
        """
        if key in self.listeners and callback in self.listeners[key]:
            self.listeners[key].remove(callback)