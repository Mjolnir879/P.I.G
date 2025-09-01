"""
Definição de mensagens de rede - estruturas de dados para comunicação
"""
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class PlayerJoinMessage:
    """Mensagem enviada quando um jogador se conecta"""
    player_id: str
    player_name: str
    position: Dict[str, float]  # {x: 100, y: 100}
    
@dataclass
class PlayerLeaveMessage:
    """Mensagem enviada quando um jogador desconecta"""
    player_id: str
    
@dataclass
class PlayerInputMessage:
    """Mensagem enviada com entrada do jogador"""
    player_id: str
    inputs: Dict[str, bool]  # {up: True, down: False, left: False, right: True}
    
@dataclass
class PlayerActionMessage:
    """Mensagem enviada com ação do jogador (ataque, uso de item, etc.)"""
    player_id: str
    action_type: str
    action_data: Dict[str, Any]
    
@dataclass
class GameStateUpdateMessage:
    """Mensagem enviada pelo servidor com atualização do estado do jogo"""
    players: Dict[str, Dict]  # Dict com todos os jogadores e seus estados
    entities: Dict[str, Dict]  # Dict com todas as entidades e seus estados
    timestamp: float
    
@dataclass
class EntityCreateMessage:
    """Mensagem enviada quando uma entidade é criada"""
    entity_id: str
    entity_type: str
    position: Dict[str, float]
    components: Dict[str, Any]
    
@dataclass
class EntityDestroyMessage:
    """Mensagem enviada quando uma entidade é destruída"""
    entity_id: str