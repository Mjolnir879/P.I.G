"""
Estado ocioso - entidade fica parada ou faz ações passivas
"""
import random
from ...core.entity_system import EntitySystem

class IdleState:
    """
    Estado ocioso - entidade não se move ou faz ações mínimas
    """
    
    def __init__(self, min_duration: float = 2.0, max_duration: float = 5.0):
        # Duração mínima do estado ocioso (segundos)
        self.min_duration = min_duration
        # Duração máxima do estado ocioso (segundos)
        self.max_duration = max_duration
        # Timer para trocar de estado
        self.timer = 0
        # Duração atual do estado
        self.current_duration = 0
        
    def enter(self, entity_id, entity_system):
        """Chamado quando o estado é ativado"""
        # Define uma duração aleatória para ficar ocioso
        self.current_duration = random.uniform(self.min_duration, self.max_duration)
        self.timer = 0
        
        # Para o movimento
        movement = entity_system.get_component(entity_id, "MovementComponent")
        if movement:
            movement.velocity_x = 0
            movement.velocity_y = 0
            
    def exit(self, entity_id, entity_system):
        """Chamado quando o estado é desativado"""
        # Nada a fazer ao sair do estado ocioso
        pass
        
    def update(self, entity_id, entity_system, dt):
        """Atualiza o estado"""
        # Atualiza o timer
        self.timer += dt
        
        # Verifica se é hora de trocar de estado
        if self.timer >= self.current_duration:
            # Sinaliza que quer trocar de estado
            # Em uma implementação real, isso seria tratado por um sistema de IA superior
            pass
            
        # Em um estado ocioso, a entidade pode fazer animações ou ações passivas
        # Por exemplo, piscar ou olhar around