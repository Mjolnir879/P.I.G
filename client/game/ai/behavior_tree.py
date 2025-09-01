"""
Implementação de árvore de comportamento para IA
"""
from abc import ABC, abstractmethod
from enum import Enum

class NodeStatus(Enum):
    """Estados possíveis para um nó da árvore de comportamento"""
    SUCCESS = 1
    FAILURE = 2
    RUNNING = 3

class BehaviorNode(ABC):
    """Classe abstrata base para todos os nós da árvore de comportamento"""
    
    @abstractmethod
    def execute(self, entity_id, entity_system, dt: float) -> NodeStatus:
        """
        Executa a lógica do nó
        Retorna o status da execução
        """
        pass

class SequenceNode(BehaviorNode):
    """
    Nó de sequência - executa filhos em ordem até que um falhe
    Retorna SUCCESS se todos os filhos retornarem SUCCESS
    Retorna FAILURE se qualquer filho retornar FAILURE
    Retorna RUNNING se qualquer filho retornar RUNNING
    """
    
    def __init__(self, children: list):
        # Lista de nós filhos
        self.children = children
        # Índice do filho atual sendo executado
        self.current_child_index = 0
        
    def execute(self, entity_id, entity_system, dt: float) -> NodeStatus:
        # Executa cada filho em sequência
        while self.current_child_index < len(self.children):
            child = self.children[self.current_child_index]
            status = child.execute(entity_id, entity_system, dt)
            
            if status == NodeStatus.FAILURE:
                # Reinicia e retorna falha
                self.current_child_index = 0
                return NodeStatus.FAILURE
            elif status == NodeStatus.RUNNING:
                # Continua executando este filho na próxima atualização
                return NodeStatus.RUNNING
            elif status == NodeStatus.SUCCESS:
                # Avança para o próximo filho
                self.current_child_index += 1
                
        # Todos os filhos foram executados com sucesso
        self.current_child_index = 0
        return NodeStatus.SUCCESS

class SelectorNode(BehaviorNode):
    """
    Nó seletor - executa filhos até que um tenha sucesso
    Retorna SUCCESS se qualquer filho retornar SUCCESS
    Retorna FAILURE se todos os filhos retornarem FAILURE
    Retorna RUNNING se qualquer filho retornar RUNNING
    """
    
    def __init__(self, children: list):
        # Lista de nós filhos
        self.children = children
        # Índice do filho atual sendo executado
        self.current_child_index = 0
        
    def execute(self, entity_id, entity_system, dt: float) -> NodeStatus:
        # Executa cada filho até que um tenha sucesso
        while self.current_child_index < len(self.children):
            child = self.children[self.current_child_index]
            status = child.execute(entity_id, entity_system, dt)
            
            if status == NodeStatus.SUCCESS:
                # Reinicia e retorna sucesso
                self.current_child_index = 0
                return NodeStatus.SUCCESS
            elif status == NodeStatus.RUNNING:
                # Continua executando este filho na próxima atualização
                return NodeStatus.RUNNING
            elif status == NodeStatus.FAILURE:
                # Avança para o próximo filho
                self.current_child_index += 1
                
        # Todos os filhos falharam
        self.current_child_index = 0
        return NodeStatus.FAILURE

class ActionNode(BehaviorNode):
    """
    Nó de ação - executa uma ação específica
    """
    
    def __init__(self, action_func):
        # Função a ser executada
        self.action_func = action_func
        
    def execute(self, entity_id, entity_system, dt: float) -> NodeStatus:
        # Executa a função de ação
        return self.action_func(entity_id, entity_system, dt)

class ConditionNode(BehaviorNode):
    """
    Nó de condição - verifica uma condição
    Retorna SUCCESS se a condição for verdadeira, FAILURE caso contrário
    """
    
    def __init__(self, condition_func):
        # Função que verifica a condição
        self.condition_func = condition_func
        
    def execute(self, entity_id, entity_system, dt: float) -> NodeStatus:
        # Verifica a condição
        if self.condition_func(entity_id, entity_system, dt):
            return NodeStatus.SUCCESS
        else:
            return NodeStatus.FAILURE

class BehaviorTree:
    """
    Árvore de comportamento - gerencia a execução de uma hierarquia de nós de comportamento
    """
    
    def __init__(self, root_node: BehaviorNode):
        # Nó raiz da árvore
        self.root_node = root_node
        
    def execute(self, entity_id, entity_system, dt: float) -> NodeStatus:
        """Executa a árvore de comportamento a partir do nó raiz"""
        return self.root_node.execute(entity_id, entity_system, dt)