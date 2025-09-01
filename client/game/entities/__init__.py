"""
Módulo de entidades - todas as entidades do jogo (player, inimigos, NPCs, etc.)
"""
# Expõe as classes de entidade principais
from .player import Player
from .enemy import Enemy
from .npc import NPC
from .entity_factory import EntityFactory