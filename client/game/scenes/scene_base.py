"""
Classe base para todas as cenas do jogo - define interface comum
"""
from abc import ABC, abstractmethod
import pygame

class SceneBase(ABC):
    """
    Classe abstrata base para todas as cenas do jogo
    Define a interface que todas as cenas devem implementar
    """
    
    def __init__(self, game):
        # Referência ao objeto principal do jogo
        self.game = game
        
    @abstractmethod
    def enter(self, *args, **kwargs):
        """
        Chamado quando a cena é ativada
        Deve inicializar recursos específicos da cena
        """
        pass
        
    @abstractmethod
    def exit(self):
        """
        Chamado quando a cena é desativada
        Deve liberar recursos específicos da cena
        """
        pass
        
    @abstractmethod
    def update(self, dt: float):
        """
        Atualiza a lógica da cena
        dt: Tempo decorrido desde a última atualização (em segundos)
        """
        pass
        
    @abstractmethod
    def render(self, surface: pygame.Surface):
        """
        Renderiza a cena na superfície fornecida
        surface: Superfície onde a cena será renderizada
        """
        pass
        
    def handle_event(self, event: pygame.event.Event):
        """
        Processa um evento específico
        Pode ser sobrescrito por cenas que precisam processar eventos
        """
        pass