"""
Lobby multiplayer - onde jogadores se conectam antes de iniciar uma partida
"""
import pygame
from .scene_base import SceneBase

class MultiplayerLobby(SceneBase):
    """
    Lobby para jogos multiplayer
    Permite que jogadores se conectem, formem grupos e iniciem partidas
    """
    
    def __init__(self, game):
        super().__init__(game)
        # Lista de jogadores no lobby
        self.players = []
        # Estado de prontidão do jogador local
        self.ready = False
        # Fonte para renderizar texto
        self.font = pygame.font.SysFont("Arial", 24)
        
    def enter(self, *args, **kwargs):
        """Inicializa o lobby multiplayer"""
        print("Entrando no lobby multiplayer")
        
        # Conecta ao servidor se não estiver conectado
        if not self.game.network_client.connected:
            self.game.network_client.connect()
            
        # Registra callbacks para mensagens de rede
        self.game.network_client.register_callback("player_joined", self.on_player_joined)
        self.game.network_client.register_callback("player_left", self.on_player_left)
        self.game.network_client.register_callback("game_starting", self.on_game_starting)
        
    def exit(self):
        """Limpa recursos do lobby"""
        print("Saindo do lobby multiplayer")
        # Desregistra callbacks para evitar referências circulares
        # (em uma implementação real, o network_client teria um método para isso)
        
    def update(self, dt: float):
        """Atualiza a lógica do lobby"""
        # Lobby não precisa de atualizações complexas
        # A maior parte da lógica é baseada em eventos de rede
        pass
        
    def render(self, surface: pygame.Surface):
        """Renderiza o lobby na tela"""
        # Preenche o fundo
        surface.fill((60, 60, 100))
        
        # Renderiza título
        title_font = pygame.font.SysFont("Arial", 36)
        title_text = title_font.render("Lobby Multiplayer", True, (255, 255, 255))
        surface.blit(title_text, (surface.get_width() // 2 - title_text.get_width() // 2, 50))
        
        # Renderiza lista de jogadores
        players_text = self.font.render("Jogadores:", True, (255, 255, 255))
        surface.blit(players_text, (50, 120))
        
        for i, player in enumerate(self.players):
            player_text = self.font.render(f"{player['name']} {'(Pronto)' if player['ready'] else ''}", True, 
                                         (0, 255, 0) if player['ready'] else (255, 255, 255))
            surface.blit(player_text, (70, 150 + i * 30))
            
        # Renderiza botão de prontidão
        ready_color = (0, 255, 0) if self.ready else (255, 0, 0)
        ready_text = self.font.render("Pronto", True, ready_color)
        pygame.draw.rect(surface, (100, 100, 100), (surface.get_width() // 2 - 75, 300, 150, 40))
        surface.blit(ready_text, (surface.get_width() // 2 - ready_text.get_width() // 2, 310))
        
        # Renderiza instruções
        instructions = self.font.render("Pressione ESPAÇO para alternar prontidão, ENTER para iniciar", True, (200, 200, 200))
        surface.blit(instructions, (surface.get_width() // 2 - instructions.get_width() // 2, 400))
        
    def handle_event(self, event: pygame.event.Event):
        """Processa eventos de entrada no lobby"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Alterna estado de prontidão
                self.toggle_ready()
            elif event.key == pygame.K_RETURN:
                # Tenta iniciar o jogo (apenas se for o líder)
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                # Volta ao menu principal
                self.game.scene_manager.switch_to("main_menu")
                
    def toggle_ready(self):
        """Alterna estado de prontidão do jogador"""
        self.ready = not self.ready
        # Envia estado de prontidão para o servidor
        self.game.network_client.send("player_ready", {"ready": self.ready})
        
    def start_game(self):
        """Tenta iniciar o jogo"""
        # Envia solicitação para iniciar o jogo
        self.game.network_client.send("start_game")
        
    def on_player_joined(self, data):
        """Callback quando um jogador entra no lobby"""
        self.players = data["players"]
        print(f"Jogador entrou no lobby. Total: {len(self.players)}")
        
    def on_player_left(self, data):
        """Callback quando um jogador sai do lobby"""
        self.players = data["players"]
        print(f"Jogador saiu do lobby. Total: {len(self.players)}")
        
    def on_game_starting(self, data):
        """Callback quando o jogo está prestes a iniciar"""
        print("Jogo iniciando...")
        # Alterna para a cena do jogo
        self.game.scene_manager.switch_to("game_world", is_multiplayer=True, map_name=data["map_name"])