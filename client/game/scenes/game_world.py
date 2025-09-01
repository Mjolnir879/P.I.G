"""
Cena principal do jogo - onde a ação acontece
"""
import pygame
import random
from .scene_base import SceneBase
from ..core.entity_system import EntitySystem
from ..entities.entity_factory import EntityFactory

class GameWorld(SceneBase):
    """
    Mundo principal do jogo - onde a jogabilidade acontece
    Pode ser singleplayer ou multiplayer
    """
    
    def __init__(self, game):
        super().__init__(game)
        # Sistema de entidades para gerenciar todas as entidades do jogo
        self.entity_system = EntitySystem()
        # Fábrica para criar entidades
        self.entity_factory = EntityFactory(self.entity_system)
        # Flag indicando se é multiplayer
        self.is_multiplayer = False
        # Mapa atual
        self.current_map = None
        # Jogador local (se singleplayer)
        self.local_player = None
        
    def enter(self, is_multiplayer: bool = False, map_name: str = "forest"):
        """
        Inicializa o mundo do jogo
        is_multiplayer: Se True, configura para modo multiplayer
        map_name: Nome do mapa a ser carregado
        """
        self.is_multiplayer = is_multiplayer
        print(f"Iniciando jogo no modo {'multiplayer' if is_multiplayer else 'singleplayer'}")
        
        # Carrega o mapa
        self.current_map = self.load_map(map_name)
        
        if not is_multiplayer:
            # Modo singleplayer - cria jogador local
            spawn_x, spawn_y = self.current_map["spawn_points"][0]
            self.local_player = self.entity_factory.create_player(spawn_x, spawn_y, True)
            
            # Gera alguns inimigos
            self.spawn_enemies(5)
        else:
            # Modo multiplayer - o jogador será criado pelo servidor
            print("Aguardando criação do jogador pelo servidor...")
            
    def exit(self):
        """Limpa recursos do mundo do jogo"""
        print("Saindo do mundo do jogo")
        # Limpa todas as entidades
        self.entity_system = EntitySystem()
        self.local_player = None
        
    def update(self, dt: float):
        """Atualiza a lógica do jogo"""
        # Atualiza todas as entidades
        for entity_id in list(self.entity_system.entities.keys()):
            # Atualiza componentes de movimento
            movement = self.entity_system.get_component(entity_id, "MovementComponent")
            if movement:
                movement.update(dt)
                
            # Atualiza componentes de combate
            combat = self.entity_system.get_component(entity_id, "CombatComponent")
            if combat:
                combat.update(dt)
                
        # Em singleplayer, atualiza a IA dos inimigos
        if not self.is_multiplayer:
            enemy_ids = self.entity_system.get_entities_with_tag("enemy")
            for enemy_id in enemy_ids:
                ai_controller = self.entity_system.get_component(enemy_id, "AIController")
                if ai_controller:
                    ai_controller.update(dt, self.entity_system)
                    
    def render(self, surface: pygame.Surface):
        """Renderiza o jogo na tela"""
        # Renderiza o fundo (em um jogo real, isso seria um tileset)
        surface.fill((0, 100, 50))  # Cor verde para grama
        
        # Renderiza todas as entidades
        for entity_id in self.entity_system.entities:
            # Obtém componente de renderização se existir
            # Em um jogo real, teríamos um componente específico para renderização
            movement = self.entity_system.get_component(entity_id, "MovementComponent")
            if movement:
                # Desenha um retângulo representando a entidade
                color = (255, 0, 0) if "enemy" in self.entity_system.tags and entity_id in self.entity_system.tags["enemy"] else (0, 0, 255)
                pygame.draw.rect(surface, color, (movement.x - 15, movement.y - 15, 30, 30))
                
        # Renderiza HUD (interface do usuário)
        self.render_hud(surface)
        
    def render_hud(self, surface: pygame.Surface):
        """Renderiza a interface do usuário"""
        # Renderiza informações do jogador
        font = pygame.font.SysFont("Arial", 18)
        
        if self.local_player:
            health = self.entity_system.get_component(self.local_player.entity_id, "HealthComponent")
            if health:
                health_text = font.render(f"Vida: {health.current_health}/{health.max_health}", True, (255, 255, 255))
                surface.blit(health_text, (10, 10))
                
        # Renderiza modo atual
        mode_text = font.render(f"Modo: {'Multiplayer' if self.is_multiplayer else 'Singleplayer'}", True, (255, 255, 255))
        surface.blit(mode_text, (10, 40))
        
    def handle_event(self, event: pygame.event.Event):
        """Processa eventos de entrada no jogo"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Volta ao menu principal
                self.game.scene_manager.switch_to("main_menu")
                
        # Se for singleplayer, repassa entrada para o jogador local
        if not self.is_multiplayer and self.local_player:
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            self.local_player.handle_input(keys, mouse_pos, mouse_buttons)
            
    def load_map(self, map_name: str) -> dict:
        """
        Carrega um mapa específico
        Em um jogo real, isso carregaria de um arquivo JSON
        """
        # Mapas pré-definidos (em um jogo real, isso viria de arquivos)
        maps = {
            "forest": {
                "name": "Floresta",
                "width": 1000,
                "height": 1000,
                "spawn_points": [(100, 100), (200, 200), (300, 300)]
            },
            "cave": {
                "name": "Caverna",
                "width": 800,
                "height": 800,
                "spawn_points": [(400, 400), (300, 300), (200, 200)]
            }
        }
        
        return maps.get(map_name, maps["forest"])
        
    def spawn_enemies(self, count: int):
        """Gera inimigos no mapa"""
        for i in range(count):
            # Escolhe um ponto de spawn aleatório
            spawn_point = random.choice(self.current_map["spawn_points"])
            x = spawn_point[0] + random.randint(-50, 50)
            y = spawn_point[1] + random.randint(-50, 50)
            
            # Escolhe um tipo de inimigo aleatório
            enemy_type = random.choice(["basic", "strong", "fast"])
            
            # Cria o inimigo
            self.entity_factory.create_enemy(x, y, enemy_type)