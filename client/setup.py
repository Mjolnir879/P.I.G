import os
import json
import yaml
from pathlib import Path

def setup_game_files():
    """Cria a estrutura de arquivos e pastas necessária para o jogo"""
    
    # Cria diretórios necessários
    directories = [
        'saves',
        'assets/data',
        'assets/images/layers',
        'server/database'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Diretório criado/verificado: {directory}")
    
    # Cria arquivo de configuração padrão se não existir
    config_path = 'saves/config.yaml'
    if not os.path.exists(config_path):
        default_config = {
            'screen': {
                'width': 800,
                'height': 600,
                'fullscreen': False
            },
            'project': {
                'window_name': 'Meu Jogo RPG',
                'FPS': 60,
                'version': '1.0.0'
            },
            'network': {
                'server_url': 'http://localhost:3000',
                'reconnect_attempts': 3,
                'timeout': 5000
            },
            'game': {
                'player_speed': 5,
                'enemy_spawn_count': 5,
                'default_map': 'forest'
            }
        }
        
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        print(f"Arquivo de configuração criado: {config_path}")
    
    # Cria arquivo do jogador padrão se não existir
    player_path = 'saves/player.json'
    if not os.path.exists(player_path):
        default_player = {
            'name': 'Jogador',
            'level': 1,
            'experience': 0,
            'health': 100,
            'max_health': 100,
            'position': {
                'x': 100,
                'y': 100,
                'map': 'forest'
            },
            'inventory': {
                'capacity': 20,
                'items': [
                    {
                        'id': 'potion_health',
                        'name': 'Poção de Vida',
                        'quantity': 3
                    },
                    {
                        'id': 'sword_wood',
                        'name': 'Espada de Madeira',
                        'quantity': 1
                    }
                ],
                'equipped': {
                    'main_hand': 'sword_wood',
                    'off_hand': None,
                    'head': None,
                    'chest': None,
                    'legs': None
                }
            },
            'stats': {
                'strength': 10,
                'dexterity': 8,
                'intelligence': 5,
                'vitality': 12
            },
            'skills': {
                'combat': 1,
                'archery': 0,
                'magic': 0,
                'crafting': 0
            }
        }
        
        with open(player_path, 'w') as f:
            json.dump(default_player, f, indent=2)
        print(f"Arquivo do jogador criado: {player_path}")
    
    # Cria arquivo de mapa básico se não existir
    map_path = 'assets/data/map.json'
    if not os.path.exists(map_path):
        # Aqui você pode adicionar a estrutura básica de um mapa
        default_map = {
            'name': 'Floresta Inicial',
            'width': 1000,
            'height': 1000,
            'tile_size': 32,
            'spawn_points': [
                {'x': 100, 'y': 100, 'type': 'player'},
                {'x': 200, 'y': 200, 'type': 'enemy'},
                {'x': 300, 'y': 300, 'type': 'npc'}
            ],
            'collision_layer': [[1]*31 for _ in range(31)],
            'entities': []
        }
        
        with open(map_path, 'w') as f:
            json.dump(default_map, f, indent=2)
        print(f"Arquivo de mapa criado: {map_path}")
    
    print("Setup concluído! O jogo está pronto para ser executado.")

if __name__ == '__main__':
    setup_game_files()