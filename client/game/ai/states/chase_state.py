"""
Estado de perseguição - faz a entidade perseguir um alvo (geralmente o jogador)
"""
from ...core.entity_system import EntitySystem

class ChaseState:
    """
    Estado de perseguição - move a entidade em direção a um alvo
    """
    
    def __init__(self, target_id: str = None):
        # ID da entidade alvo
        self.target_id = target_id
        # Distância mínima para manter do alvo
        self.min_distance = 50.0
        
    def enter(self, entity_id, entity_system):
        """Chamado quando o estado é ativado"""
        # Se nenhum alvo foi especificado, tenta encontrar o jogador
        if self.target_id is None:
            self.target_id = self.find_player(entity_system)
            
    def exit(self, entity_id, entity_system):
        """Chamado quando o estado é desativado"""
        # Para o movimento
        movement = entity_system.get_component(entity_id, "MovementComponent")
        if movement:
            movement.velocity_x = 0
            movement.velocity_y = 0
            
    def update(self, entity_id, entity_system, dt):
        """Atualiza o estado"""
        if self.target_id is None:
            return  # Não há alvo para perseguir
            
        # Obtém a posição do alvo
        target_movement = entity_system.get_component(self.target_id, "MovementComponent")
        if target_movement is None:
            return  # Alvo não tem componente de movimento
            
        # Obtém a posição da entidade atual
        movement = entity_system.get_component(entity_id, "MovementComponent")
        if movement is None:
            return  # Entidade atual não tem componente de movimento
            
        # Calcula a direção até o alvo
        dx = target_movement.x - movement.x
        dy = target_movement.y - movement.y
        distance = (dx**2 + dy**2)**0.5
        
        # Se estiver muito perto, para de perseguir
        if distance < self.min_distance:
            movement.velocity_x = 0
            movement.velocity_y = 0
            return
            
        # Normaliza a direção
        if distance > 0:
            dx /= distance
            dy /= distance
            
        # Move em direção ao alvo
        movement.velocity_x = dx * movement.speed
        movement.velocity_y = dy * movement.speed
        
    def find_player(self, entity_system) -> str:
        """
        Encontra o ID do jogador
        Retorna o ID da primeira entidade com tag "player", ou None se não encontrar
        """
        players = entity_system.get_entities_with_tag("player")
        if players:
            return next(iter(players))  # Retorna o primeiro jogador
        return None