"""
Componente de combate - gerencia ataques, dano e habilidades de combate
"""
import time
from typing import Optional

class CombatComponent:
    """
    Componente que adiciona capacidades de combate a uma entidade
    Permite ataques, habilidades e gerenciamento de cooldowns
    """
    
    def __init__(self, base_damage: int = 10, attack_range: float = 50.0, attack_cooldown: float = 1.0):
        # Dano base dos ataques
        self.base_damage = base_damage
        # Alcance do ataque
        self.attack_range = attack_range
        # Tempo de recarga entre ataques
        self.attack_cooldown = attack_cooldown
        # Tempo do último ataque
        self.last_attack_time = 0
        # Alvo atual do ataque
        self.attack_target = None
        
    def can_attack(self) -> bool:
        """
        Verifica se a entidade pode atacar (cooldown terminou)
        Retorna True se pode atacar, False caso contrário
        """
        current_time = time.time()
        return current_time - self.last_attack_time >= self.attack_cooldown
        
    def attack(self, target_x: float, target_y: float, entity_system, attacker_id: str) -> bool:
        """
        Executa um ataque em uma posição-alvo
        target_x, target_y: Posição do alvo
        entity_system: Referência ao sistema de entidades
        attacker_id: ID da entidade atacante
        Retorna True se o ataque foi bem-sucedido, False caso contrário
        """
        # Verifica se pode atacar
        if not self.can_attack():
            return False
            
        # Marca o tempo do ataque
        self.last_attack_time = time.time()
        
        # Encontra entidades no alcance do ataque
        hit_entity = self.find_target_in_range(target_x, target_y, entity_system, attacker_id)
        
        if hit_entity:
            # Aplica dano à entidade atingida
            health_component = entity_system.get_component(hit_entity, "HealthComponent")
            if health_component:
                health_component.take_damage(self.base_damage)
                return True
                
        return False
        
    def find_target_in_range(self, target_x: float, target_y: float, entity_system, exclude_id: str) -> Optional[str]:
        """
        Encontra uma entidade dentro do alcance do ataque
        target_x, target_y: Posição do alvo
        entity_system: Referência ao sistema de entidades
        exclude_id: ID da entidade a excluir (normalmente o atacante)
        Retorna o ID da entidade atingida, ou None se nenhuma for atingida
        """
        # Itera por todas as entidades que têm componente de saúde
        for entity_id in entity_system.get_entities_with_component("HealthComponent"):
            if entity_id == exclude_id:
                continue  # Pula o atacante
                
            # Obtém componente de movimento para verificar a posição
            movement = entity_system.get_component(entity_id, "MovementComponent")
            if movement:
                # Calcula a distância até o alvo
                dx = movement.x - target_x
                dy = movement.y - target_y
                distance = (dx**2 + dy**2)**0.5
                
                # Verifica se está dentro do alcance
                if distance <= self.attack_range:
                    return entity_id
                    
        return None
        
    def get_remaining_cooldown(self) -> float:
        """
        Retorna o tempo restante de cooldown em segundos
        """
        current_time = time.time()
        elapsed = current_time - self.last_attack_time
        return max(0, self.attack_cooldown - elapsed)