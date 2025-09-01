"""
Módulo de IA - sistemas de inteligência artificial para entidades não jogáveis
"""
# Expõe as classes de IA principais
from .behavior_tree import BehaviorTree, SequenceNode, SelectorNode, ActionNode, ConditionNode
from .ai_controller import AIController
from .states.wander_state import WanderState
from .states.chase_state import ChaseState
from .states.idle_state import IdleState