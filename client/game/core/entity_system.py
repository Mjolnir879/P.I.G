"""
Sistema de gerenciamento de entidades do jogo
Implementa o padrão ECS (Entity-Component-System) para gerenciamento flexível de entidades
"""
import uuid
from typing import Dict, List, Set, Any, Optional

class EntitySystem:
    """Sistema principal para gerenciar todas as entidades do jogo e seus componentes"""
    
    def __init__(self):
        # Dicionário principal que armazena todas as entidades e seus componentes
        self.entities: Dict[str, Dict[str, Any]] = {}
        # Indexação rápida de componentes por tipo
        self.components: Dict[str, Dict[str, Any]] = {}
        # Sistema de tags para agrupamento de entidades
        self.tags: Dict[str, Set[str]] = {}
        
    def create_entity(self, *components) -> str:
        """
        Cria uma nova entidade com componentes opcionais
        Retorna um ID único para a entidade
        """
        # Gera um ID único usando UUID
        entity_id = str(uuid.uuid4())
        # Inicializa a entidade com um dicionário vazio de componentes
        self.entities[entity_id] = {}
        
        # Adiciona cada componente fornecido à entidade
        for component in components:
            self.add_component(entity_id, component)
            
        return entity_id
        
    def add_component(self, entity_id: str, component: Any) -> None:
        """
        Adiciona um componente a uma entidade específica
        Mantém indexação para acesso rápido por tipo de componente
        """
        # Obtém o nome da classe do componente como chave
        component_type = type(component).__name__
        
        # Inicializa o dicionário para este tipo de componente se não existir
        if component_type not in self.components:
            self.components[component_type] = {}
            
        # Adiciona o componente à indexação por tipo
        self.components[component_type][entity_id] = component
        # Adiciona o componente à entidade específica
        self.entities[entity_id][component_type] = component
        
    def get_component(self, entity_id: str, component_type: str) -> Optional[Any]:
        """
        Obtém um componente específico de uma entidade
        Retorna None se o componente não existir
        """
        return self.entities[entity_id].get(component_type)
        
    def get_entities_with_component(self, component_type: str) -> List[str]:
        """
        Obtém todas as entidades que possuem um componente específico
        Útil para sistemas que precisam processar apenas entidades com certos componentes
        """
        return list(self.components.get(component_type, {}).keys())
        
    def add_tag(self, entity_id: str, tag: str) -> None:
        """
        Adiciona uma tag a uma entidade para agrupamento e identificação
        Tags são úteis para categorizar entidades (ex: "player", "enemy", "item")
        """
        if tag not in self.tags:
            self.tags[tag] = set()
        self.tags[tag].add(entity_id)
        
    def get_entities_with_tag(self, tag: str) -> Set[str]:
        """
        Obtém todas as entidades com uma tag específica
        Retorna um conjunto vazio se a tag não existir
        """
        return self.tags.get(tag, set())
        
    def remove_entity(self, entity_id: str) -> None:
        """
        Remove completamente uma entidade do sistema
        Limpa todos os componentes e referências
        """
        if entity_id in self.entities:
            # Remove todos os componentes da indexação
            for component_type in self.entities[entity_id]:
                if component_type in self.components and entity_id in self.components[component_type]:
                    del self.components[component_type][entity_id]
            
            # Remove a entidade do registro principal
            del self.entities[entity_id]
            
            # Remove a entidade de todas as tags
            for tag in self.tags:
                if entity_id in self.tags[tag]:
                    self.tags[tag].remove(entity_id)