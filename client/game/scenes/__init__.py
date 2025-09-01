"""
Módulo de cenas - todas as cenas/estados do jogo (menu, jogo, etc.)
"""
# Expõe as classes de cena principais
from .scene_base import SceneBase
from .main_menu import MainMenu
from .game_world import GameWorld
from .multiplayer_lobby import MultiplayerLobby