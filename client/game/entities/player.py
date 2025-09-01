"""
Implementação da entidade jogador - controlada pelo usuário
"""
import pygame
from typing import Dict, Any
from ..core.entity_system import EntitySystem
from ..components.movement import MovementComponent
from ..components.health import HealthComponent
from ..components.inventory import InventoryComponent
from ..components.combat import CombatComponent

class Player:
    """
    Representa o jogador no jogo
    Controlada por entrada do usuário (teclado/mouse)
    Pode ser usada em modo singleplayer ou multiplayer
    """
    
    def __init__(self, entity_system: EntitySystem, x: float, y: float, is_local: bool = True):
        """
        Inicializa um novo jogador
        entity_system: Referência ao sistema de entidades
        x, y: Posição inicial do jogador
        is_local: Se True, o jogador é controlado localmente
        """
        # Cria uma nova entidade no sistema
        self.entity_id = entity_system.create_entity()
        # Referência ao sistema de entidades
        self.entity_system = entity_system
        # Flag indicando se é o jogador local
        self.is_local = is_local
        
        # Adiciona componentes básicos ao jogador
        entity_system.add_component(self.entity_id, MovementComponent(x, y))
        entity_system.add_component(self.entity_id, HealthComponent(100))
        entity_system.add_component(self.entity_id, InventoryComponent())
        entity_system.add_component(self.entity_id, CombatComponent(10))
        
        # Marca como jogador no sistema de tags
        entity_system.add_tag(self.entity_id, "player")
        
        # Se for jogador local, marca com tag adicional
        if is_local:
            entity_system.add_tag(self.entity_id, "local_player")
            
    def handle_input(self, keys: Dict[int, bool], mouse_pos: tuple, mouse_buttons: tuple) -> None:
        """
        Processa entrada do usuário para controlar o jogador
        keys: Dicionário com estado das teclas (pygame.key.get_pressed())
        mouse_pos: Posição atual do mouse (x, y)
        mouse_buttons: Estado dos botões do mouse
        """
        if not self.is_local:
            return  # Apenas processa entrada se for jogador local
            
        # Obtém o componente de movimento
        movement = self.entity_system.get_component(self.entity_id, "MovementComponent")
        
        if movement:
            # Reseta a velocidade
            movement.velocity_x = 0
            movement.velocity_y = 0
            
            # Define velocidade baseada nas teclas pressionadas
            if keys[pygame.K_w]:
                movement.velocity_y = -5
            if keys[pygame.K_s]:
                movement.velocity_y = 5
            if keys[pygame.K_a]:
                movement.velocity_x = -5
            if keys[pygame.K_d]:
                movement.velocity_x = 5
                
            # Normaliza a velocidade para movimento diagonal
            if movement.velocity_x != 0 and movement.velocity_y != 0:
                movement.velocity_x *= 0.7071  # √2/2 para normalizar
                movement.velocity_y *= 0.7071
                
            # Processa ataque com botão esquerdo do mouse
            if mouse_buttons[0]:  # Botão esquerdo pressionado
                combat = self.entity_system.get_component(self.entity_id, "CombatComponent")
                if combat:
                    combat.attack(mouse_pos)
                    
    def get_position(self) -> tuple:
        """Obtém a posição atual do jogador"""
        movement = self.entity_system.get_component(self.entity_id, "MovementComponent")
        if movement:
            return (movement.x, movement.y)
        return (0, 0)
        
    def set_position(self, x: float, y: float) -> None:
        """Define a posição do jogador"""
        movement = self.entity_system.get_component(self.entity_id, "MovementComponent")
        if movement:
            movement.x = x
            movement.y = y