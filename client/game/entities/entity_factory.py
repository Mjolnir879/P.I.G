"""
Fábrica de entidades - cria e configura entidades de forma consistente
"""
from typing import Dict, Any
from .player import Player
from .enemy import Enemy
from .npc import NPC
from ..core.entity_system import EntitySystem

class EntityFactory:
    """
    Fábrica para criar entidades do jogo de forma consistente
    Centraliza a criação de entidades para garantir configuração uniforme
    """
    
    def __init__(self, entity_system: EntitySystem):
        # Referência ao sistema de entidades
        self.entity_system = entity_system
        # Configurações pré-definidas para cada tipo de entidade
        self.entity_configs = self.load_entity_configs()
        
    def load_entity_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Carrega configurações para cada tipo de entidade
        Em um jogo real, isso viria de arquivos JSON ou de banco de dados
        """
        return {
            "player": {
                "health": 100,
                "speed": 5,
                "damage": 10
            },
            "enemy_basic": {
                "health": 50,
                "speed": 2,
                "damage": 5
            },
            "enemy_strong": {
                "health": 100,
                "speed": 1.5,
                "damage": 10
            },
            "enemy_fast": {
                "health": 30,
                "speed": 3.5,
                "damage": 3
            },
            "npc_merchant": {
                "speed": 1,
                "dialogue": "initial_merchant"
            }
        }
        
    def create_player(self, x: float, y: float, is_local: bool = True) -> Player:
        """
        Cria uma nova entidade jogador
        x, y: Posição inicial
        is_local: Se True, é o jogador local
        """
        return Player(self.entity_system, x, y, is_local)
        
    def create_enemy(self, x: float, y: float, enemy_type: str = "basic") -> Enemy:
        """
        Cria uma nova entidade inimigo
        x, y: Posição inicial
        enemy_type: Tipo do inimigo (basic, strong, fast)
        """
        return Enemy(self.entity_system, x, y, enemy_type)
        
    def create_npc(self, x: float, y: float, npc_type: str, dialogue_tree: dict) -> NPC:
        """
        Cria uma nova entidade NPC
        x, y: Posição inicial
        npc_type: Tipo do NPC
        dialogue_tree: Árvore de diálogo para interações
        """
        return NPC(self.entity_system, x, y, npc_type, dialogue_tree)
        
    def create_from_template(self, template_name: str, x: float, y: float) -> Any:
        """
        Cria uma entidade a partir de um template pré-definido
        Útil para criação em massa de entidades similares
        """
        if template_name not in self.entity_configs:
            print(f"Erro: Template '{template_name}' não encontrado.")
            return None
            
        config = self.entity_configs[template_name]
        
        if template_name == "player":
            return self.create_player(x, y)
        elif template_name.startswith("enemy_"):
            enemy_type = template_name.split("_")[1]
            return self.create_enemy(x, y, enemy_type)
        elif template_name.startswith("npc_"):
            npc_type = template_name.split("_")[1]
            # Em um jogo real, carregaria a árvore de diálogo de um arquivo
            dialogue_tree = {"initial": {"text": "Olá!", "choices": []}}
            return self.create_npc(x, y, npc_type, dialogue_tree)
            
        return None