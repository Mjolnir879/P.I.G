"""
Controlador de IA - gerencia o comportamento de entidades não jogáveis
"""
from .behavior_tree import BehaviorTree, SequenceNode, SelectorNode, ActionNode, ConditionNode
from ..core.entity_system import EntitySystem

class AIController:
    """
    Controlador de IA para entidades não jogáveis
    Utiliza árvore de comportamento para tomar decisões
    """
    
    def __init__(self):
        # Árvore de comportamento da entidade
        self.behavior_tree = self.create_behavior_tree()
        # Estado atual da IA
        self.current_state = "idle"
        # Timer para troca de estados
        self.state_timer = 0
        
    def create_behavior_tree(self) -> BehaviorTree:
        """
        Cria a árvore de comportamento para esta entidade
        Em um jogo real, isso seria personalizado por tipo de entidade
        """
        # Nós de condição
        can_see_player = ConditionNode(self.can_see_player)
        is_low_health = ConditionNode(self.is_low_health)
        is_idle_time_over = ConditionNode(self.is_idle_time_over)
        
        # Nós de ação
        wander_action = ActionNode(self.wander)
        chase_action = ActionNode(self.chase)
        flee_action = ActionNode(self.flee)
        idle_action = ActionNode(self.idle)
        
        # Comportamento de fuga (prioridade máxima)
        flee_behavior = SequenceNode([is_low_health, flee_action])
        
        # Comportamento de perseguição
        chase_behavior = SequenceNode([can_see_player, chase_action])
        
        # Comportamento de vagar
        wander_behavior = SequenceNode([is_idle_time_over, wander_action])
        
        # Comportamento inativo
        idle_behavior = SequenceNode([idle_action])
        
        # Árvore de decisão principal (seletor)
        root_node = SelectorNode([
            flee_behavior,      # Primeiro tenta fugir se estiver com pouca vida
            chase_behavior,     # Depois tenta perseguir se vir o jogador
            wander_behavior,    # Depois vagueia se o tempo ocioso acabou
            idle_behavior       # Finalmente fica ocioso
        ])
        
        return BehaviorTree(root_node)
        
    def update(self, dt: float, entity_system: EntitySystem) -> None:
        """
        Atualiza o comportamento da IA
        dt: Tempo decorrido desde a última atualização
        entity_system: Referência ao sistema de entidades
        """
        # Executa a árvore de comportamento
        # Em uma implementação real, precisaríamos da entity_id
        # status = self.behavior_tree.execute(entity_id, entity_system, dt)
        pass
        
    def can_see_player(self, entity_id, entity_system, dt) -> bool:
        """Verifica se a entidade pode ver o jogador"""
        # Em uma implementação real, verificaria visão e distância
        return False
        
    def is_low_health(self, entity_id, entity_system, dt) -> bool:
        """Verifica se a entidade está com pouca saúde"""
        # Em uma implementação real, verificaria o componente de saúde
        return False
        
    def is_idle_time_over(self, entity_id, entity_system, dt) -> bool:
        """Verifica se o tempo ocioso acabou"""
        # Em uma implementação real, usaria um timer
        return True
        
    def wander(self, entity_id, entity_system, dt) -> bool:
        """Ação de vagar aleatoriamente"""
        # Em uma implementação real, implementaria movimento aleatório
        return True
        
    def chase(self, entity_id, entity_system, dt) -> bool:
        """Ação de perseguir o jogador"""
        # Em uma implementação real, implementaria perseguição
        return True
        
    def flee(self, entity_id, entity_system, dt) -> bool:
        """Ação de fugir do jogador"""
        # Em uma implementação real, implementaria fuga
        return True
        
    def idle(self, entity_id, entity_system, dt) -> bool:
        """Ação de ficar ocioso"""
        # Em uma implementação real, implementaria comportamento ocioso
        return True