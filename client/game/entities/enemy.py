"""
Implementação da entidade inimigo - controlada por IA
"""
import random
from ..core.entity_system import EntitySystem
from ..components.movement import MovementComponent
from ..components.health import HealthComponent
from ..components.combat import CombatComponent
from ..ai.ai_controller import AIController

class Enemy:
    """
    Representa um inimigo no jogo
    Controlado por sistema de IA
    Pode perseguir, atacar ou fugir do jogador
    """
    
    def __init__(self, entity_system: EntitySystem, x: float, y: float, enemy_type: str = "basic"):
        """
        Inicializa um novo inimigo
        entity_system: Referência ao sistema de entidades
        x, y: Posição inicial do inimigo
        enemy_type: Tipo do inimigo (define atributos e comportamento)
        """
        # Cria uma nova entidade no sistema
        self.entity_id = entity_system.create_entity()
        self.entity_system = entity_system
        self.enemy_type = enemy_type
        
        # Configura atributos baseados no tipo
        health = 50
        damage = 5
        speed = 2
        
        if enemy_type == "strong":
            health = 100
            damage = 10
            speed = 1.5
        elif enemy_type == "fast":
            health = 30
            damage = 3
            speed = 3.5
            
        # Adiciona componentes ao inimigo
        entity_system.add_component(self.entity_id, MovementComponent(x, y, speed))
        entity_system.add_component(self.entity_id, HealthComponent(health))
        entity_system.add_component(self.entity_id, CombatComponent(damage))
        
        # Adiciona controlador de IA
        entity_system.add_component(self.entity_id, AIController())
        
        # Marca como inimigo no sistema de tags
        entity_system.add_tag(self.entity_id, "enemy")
        entity_system.add_tag(self.entity_id, enemy_type)  # Tag específica por tipo