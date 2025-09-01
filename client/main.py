import pygame
import sys
import socketio
import os
import yaml
import subprocess
import socket
import time
from enum import Enum, auto

class Player:
    """Representação simples de um jogador como sprite quadrado."""
    def __init__(self, x: float, y: float, size: int = 50, color=(200, 50, 50)):
        self.x = float(x)
        self.y = float(y)
        self.size = size
        self.color = color

    def render(self, surface: pygame.Surface):

        rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        pygame.draw.rect(surface, self.color, rect)

# Configurações do jogo :cite[4]
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Estados do jogo
class GameState(Enum):
    MAIN_MENU = auto()
    SINGLEPLAYER = auto()
    MULTIPLAYER_MENU = auto()
    MULTIPLAYER = auto()
    OPTIONS = auto()

class GameClient:
    def __init__(self):
        # Inicialização do Pygame :cite[4]
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Game with LAN Multiplayer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState.MAIN_MENU
        
        # Conexão de rede
        self.socket = socketio.Client()
        self.socket = socketio.Client()
        self.connected = False
        self.player_id = None              # <-- inicializa aqui para evitar AttributeError
        self.setup_network_handlers()
        
        # Recursos do jogo
        self.load_resources()

        self.menu_options = ["Singleplayer", "Multiplayer", "Options", "Quit"]
        self.selected_option = 0 
        self.multiplayer_menu_options = [
            "Host (localhost)",
            "Host (LAN - 0.0.0.0)",
            "Connect to address...",
            "Back"
        ]
        self.multiplayer_selected = 0
        self.server_process = None
        self.server_hosting = False
        self.server_url_override = None

    def load_resources(self):
        """Carrega todos os recursos do jogo"""
        self.font = pygame.font.SysFont('Arial', 24)
        self.players = {}
        self.local_player = None
        self.entities = []

    def get_local_ip(self) -> str:
        """Retorna um IP local utilisável na LAN (não 127.0.0.1)"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.5)
            # conecta a IP público qualquer para descobrir a interface de saída
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def start_local_server(self, host: str = "127.0.0.1") -> bool:
        """
        Inicia o servidor Node local (server/index.js).
        host: '127.0.0.1' ou '0.0.0.0'
        Retorna True se o processo foi iniciado.
        Requer Node.js e dependências instaladas em ../server.
        """
        if self.server_process:
            print("Servidor já em execução.")
            return True
        server_dir = os.path.join(os.path.dirname(__file__), "..", "server")
        server_dir = os.path.abspath(server_dir)
        if not os.path.exists(os.path.join(server_dir, "index.js")):
            print(f"Não foi encontrado index.js em {server_dir}")
            return False

        env = os.environ.copy()
        env["HOST"] = host
        # Opcionalmente pode-se setar PORT via env
        try:
            # Inicia servidor em processo separado
            self.server_process = subprocess.Popen(
                ["node", "index.js"],
                cwd=server_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )
            # Pequena espera para permitir boot do servidor
            time.sleep(0.6)
            self.server_hosting = True
            print(f"Servidor iniciado em {host} (PID {self.server_process.pid})")
            return True
        except Exception as e:
            print(f"Falha ao iniciar servidor: {e}")
            self.server_process = None
            self.server_hosting = False
            return False
        
    def stop_local_server(self):
        """Encerra o servidor iniciado por start_local_server()"""
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=2)
            except Exception:
                try:
                    self.server_process.kill()
                except Exception:
                    pass
            print("Servidor local encerrado.")
        self.server_process = None
        self.server_hosting = False

    def setup_network_handlers(self):
        """Configura os manipuladores de eventos de rede"""
        @self.socket.on('connect')
        def on_connect():
            print("Conectado ao servidor")
            self.connected = True
            if self.game_state == GameState.MULTIPLAYER:
                start_x = SCREEN_WIDTH // 2 - 25
                start_y = SCREEN_HEIGHT // 2 - 25
                join_payload = {
                    'x': start_x,
                    'y': start_y,
                    'size': 50,
                    'color': (50, 150, 200)
                }
                try:
                    self.socket.emit('join', join_payload)
                except Exception as e:
                    print(f"Erro emit join: {e}")

            
        @self.socket.on('disconnect')
        def on_disconnect():
            print("Desconectado do servidor")
            self.connected = False
            self.player_id = None

        @self.socket.on('game_state')
        def on_game_state(data):
            """Compat: servidor envia 'game_state'"""
            self.handle_server_update(data)
            
        @self.socket.on('game_state_update')
        def on_game_state_update(data):
            """Atualiza o estado do jogo com dados do servidor"""
            self.handle_server_update(data)

        @self.socket.on('welcome')
        def on_welcome(data):
            """Recebe player_id e estado inicial do servidor"""
            self.player_id = data.get('player_id')
            state = data.get('state', {})
            players = state.get('players', {})
            # construir players locais como instâncias Player
            self.handle_server_update(state)
            
            print(f"Welcome: assigned id = {self.player_id}")

        @self.socket.on('player_joined')
        def on_player_joined(data):
            pid = data.get('id')
            pdata = data.get('player', {})
            if pid and pid != self.player_id:
                self.players[pid] = Player(
                    pdata.get('x', 0),
                    pdata.get('y', 0),
                    size=pdata.get('size', 50),
                    color=tuple(pdata.get('color', (200,50,50)))
                )
                print(f"Player joined: {pid}")

        @self.socket.on('player_left')
        def on_player_left(data):
            pid = data.get('id')
            if pid in self.players:
                del self.players[pid]
                print(f"Player left: {pid}")

        @self.socket.on('player_update')
        def on_player_update(data):
            pid = data.get('id')
            pdata = data.get('player', {})
            if pid in self.players:
                p = self.players[pid]
                p.x = pdata.get('x', p.x)
                p.y = pdata.get('y', p.y)
                # opcional: size/color updates
            
    def handle_server_update(self, data):
        """Processa atualizações do servidor"""
        if self.game_state != GameState.MULTIPLAYER:
            return  # Ignora se não estiver em multiplayer
        players = data.get('players', {}) if isinstance(data, dict) else {}
        new_players = {}
        for pid, pdata in players.items():
            try:
                color = tuple(pdata.get('color', (200, 50, 50)))
            except Exception:
                color = (200, 50, 50)
            new_players[pid] = Player(
                pdata.get('x', 0),
                pdata.get('y', 0),
                size=pdata.get('size', 50),
                color=color
            )
        self.players = new_players

        # Entities: criar stubs simples com render(surface)
        self.entities = []
        raw_entities = data.get('entities', []) if isinstance(data, dict) else []
        for ent in raw_entities:
            if not isinstance(ent, dict):
                continue
            e = type("EntityStub", (), {})()
            e.x = ent.get('x', 0)
            e.y = ent.get('y', 0)
            e.size = ent.get('size', 30)
            color = tuple(ent.get('color', (150, 150, 150)))
            def _render(self_obj, surface, _color=color):
                pygame.draw.rect(surface, _color, (int(self_obj.x), int(self_obj.y), self_obj.size, self_obj.size))
            e.render = _render.__get__(e, e.__class__)
            # opcional: métodos adicionais (take_damage, etc.) podem ser adicionados se necessário
            self.entities.append(e)
    
    def safe_emit(self, event, data=None):
        """Envia mensagens apenas se conectado ao servidor"""
        if self.connected:
            try:
                self.socket.emit(event, data)
                return True
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
                return False
        else:
            print(f"Tentativa de enviar '{event}' sem conexão com o servidor")
            return False

    def handle_events(self):
        """Processa eventos de entrada"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Processa eventos do teclado
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
                
            # Processa eventos do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)
                
            if event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
        
        # Captura de entrada contínua
        keys = pygame.key.get_pressed()
        movement_input = {
            'up': keys[pygame.K_w],
            'down': keys[pygame.K_s],
            'left': keys[pygame.K_a],
            'right': keys[pygame.K_d]
        }
        
        # Envia entrada para o servidor em modo multiplayer
        if self.game_state == GameState.MULTIPLAYER:
            self.socket.emit('player_input', movement_input)
        elif self.game_state == GameState.SINGLEPLAYER:
            self.handle_local_input(movement_input)
    
    def handle_keydown(self, event):
        """Processa pressionamento de teclas"""
        if self.game_state == GameState.MAIN_MENU:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self.select_menu_option()
        elif self.game_state == GameState.MULTIPLAYER_MENU:
            if event.key == pygame.K_UP:
                self.multiplayer_selected = (self.multiplayer_selected - 1) % len(self.multiplayer_menu_options)
            elif event.key == pygame.K_DOWN:
                self.multiplayer_selected = (self.multiplayer_selected + 1) % len(self.multiplayer_menu_options)
            elif event.key == pygame.K_RETURN:
                self.handle_multiplayer_menu_selection()
            elif event.key == pygame.K_ESCAPE:
                self.game_state = GameState.MAIN_MENU


    def handle_mouse_click(self, event):
        """Processa cliques do mouse"""
        if self.game_state == GameState.MAIN_MENU and event.button == 1:  # Botão esquerdo
            mouse_pos = pygame.mouse.get_pos()
            self.check_menu_click(mouse_pos)
        elif self.game_state == GameState.MULTIPLAYER_MENU and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            for i in range(len(self.multiplayer_menu_options)):
                y = 180 + i * 48
                rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y - 8, 400, 40)
                if rect.collidepoint((mx, my)):
                    self.multiplayer_selected = i
                    self.handle_multiplayer_menu_selection()
                    break

    def handle_mouse_motion(self, event):
        """Processa movimento do mouse para highlight de opções"""
        if self.game_state == GameState.MAIN_MENU:
            mouse_pos = pygame.mouse.get_pos()
            self.update_menu_selection(mouse_pos)
        elif self.game_state == GameState.MULTIPLAYER_MENU:
            mx, my = pygame.mouse.get_pos()
            for i in range(len(self.multiplayer_menu_options)):
                y = 180 + i * 48
                rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y - 8, 400, 40)
                if rect.collidepoint((mx, my)):
                    self.multiplayer_selected = i
                    break

    def check_menu_click(self, mouse_pos):
        """Verifica se o clique foi em uma opção do menu"""
        for i, option in enumerate(self.menu_options):
            option_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - 150,
                200 + i * 50,
                300,
                40
            )
            if option_rect.collidepoint(mouse_pos):
                self.selected_option = i
                self.select_menu_option()
                break

    def update_menu_selection(self, mouse_pos):
        """Atualiza a seleção do menu com base na posição do mouse"""
        for i, option in enumerate(self.menu_options):
            option_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - 150,
                200 + i * 50,
                300,
                40
            )
            if option_rect.collidepoint(mouse_pos):
                self.selected_option = i
                break

    def select_menu_option(self):
        """Processa a opção selecionada no menu"""
        option = self.menu_options[self.selected_option]
        
        if option == "Singleplayer":
            self.game_state = GameState.SINGLEPLAYER
            self.initialize_singleplayer()
        elif option == "Multiplayer":
            self.game_state = GameState.MULTIPLAYER_MENU
            self.multiplayer_selected = 0
        elif option == "Options":
            self.game_state = GameState.OPTIONS
            # TODO: Implementar tela de opções
        elif option == "Quit":
            if self.server_hosting:
                self.stop_local_server()
            self.running = False

    def initialize_singleplayer(self):
        """Inicializa o modo singleplayer"""
        print("Iniciando modo singleplayer...")
        # TODO: Implementar inicialização do singleplayer
        start_x = SCREEN_WIDTH // 2 - 25
        start_y = SCREEN_HEIGHT // 2 - 25
        self.local_player = Player(start_x, start_y, size=50, color=(50, 150, 200))
        # Limpa ou inicializa entidades locais
        self.entities = []
    
    def initialize_multiplayer(self, server_url: str = None):
        """Inicializa o modo multiplayer; server_url opcional (ex: 'http://localhost:3000')."""
        print("Iniciando modo multiplayer...")
        # se foi passado explicitamente, prioriza
        if server_url is None:
            server_url = os.environ.get('GAME_SERVER_URL', None)
            if not server_url:
                try:
                    with open(r"c:\Users\Isaqu\Documents\Visual Studio Code\Teste_RPG065\saves\config.yaml", "r") as f:
                        cfg = yaml.safe_load(f)
                    server_url = cfg.get("network", {}).get("server_url")
                except Exception:
                    server_url = None

        # fallback: localhost
        if not server_url:
            server_url = "http://localhost:3000"

        print(f"Tentando conectar em {server_url} ...")
        try:
            self.socket.connect(server_url)
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
            self.game_state = GameState.MAIN_MENU


    def handle_multiplayer_menu_selection(self):
        """Executa ação para a opção selecionada no multiplayer submenu"""
        option = self.multiplayer_menu_options[self.multiplayer_selected]

        if option == "Host (localhost)":
            ok = self.start_local_server("127.0.0.1")
            if ok:
                # Conectar o cliente ao server local
                self.server_url_override = "http://localhost:3000"
                self.initialize_multiplayer(self.server_url_override)
                self.game_state = GameState.MULTIPLAYER
        elif option == "Host (LAN - 0.0.0.0)":
            ok = self.start_local_server("0.0.0.0")
            if ok:
                lan_ip = self.get_local_ip()
                # para o cliente local, conectar via localhost é OK; para outros use lan_ip
                self.server_url_override = f"http://localhost:3000"
                self.initialize_multiplayer(self.server_url_override)
                self.game_state = GameState.MULTIPLAYER
                print(f"Server listening for LAN at http://{lan_ip}:3000")
        elif option == "Connect to address...":
            # Prompt simples no terminal (UI mínima); pode ser substituído por caixa de diálogo
            print("Digite o endereço do servidor (ex: http://192.168.1.42:3000) e pressione Enter:")
            addr = input().strip()
            if addr:
                self.server_url_override = addr
                self.initialize_multiplayer(self.server_url_override)
                self.game_state = GameState.MULTIPLAYER
            else:
                print("Endereço vazio — ação cancelada.")
        elif option == "Back":
            self.game_state = GameState.MAIN_MENU


    def handle_attack(self):
        """Processa ação de ataque"""
        mouse_pos = pygame.mouse.get_pos()
        attack_data = {
            'type': 'attack',
            'target_x': mouse_pos[0],
            'target_y': mouse_pos[1],
            'timestamp': pygame.time.get_ticks()
        }
        
        if self.game_state == GameState.MULTIPLAYER:
            self.socket.emit('player_action', attack_data)
        else:
            self.process_attack(attack_data)
    
    def process_attack(self, attack_data):
        """Processa ataque localmente"""
        # Lógica de ataque para singleplayer
        for entity in self.entities:
            distance = ((entity.x - attack_data['target_x'])**2 + 
                       (entity.y - attack_data['target_y'])**2)**0.5
            if distance < 50:  # Raio de ataque
                entity.take_damage(10)
    
    def handle_local_input(self, movement_input):
        """Processa entrada para singleplayer"""
        if self.local_player:
            speed = 5
            if movement_input['up']:
                self.local_player.y -= speed
            if movement_input['down']:
                self.local_player.y += speed
            if movement_input['left']:
                self.local_player.x -= speed
            if movement_input['right']:
                self.local_player.x += speed
            
            # Mantém o jogador dentro dos limites da tela
            self.local_player.x = max(0, min(SCREEN_WIDTH - 50, self.local_player.x))
            self.local_player.y = max(0, min(SCREEN_HEIGHT - 50, self.local_player.y))
    
    def update(self):
        """Atualiza a lógica do jogo"""
        if self.game_state == GameState.SINGLEPLAYER:
            self.update_singleplayer()
        elif self.game_state == GameState.MULTIPLAYER:
            self.update_multiplayer()
    
    def update_singleplayer(self):
        """Atualiza lógica do singleplayer"""
        for entity in self.entities:
            if hasattr(entity, 'ai_controller'):
                entity.ai_controller.update()
    
    def update_multiplayer(self):
        """Atualiza lógica do multiplayer - o servidor é a autoridade"""
        # Em multiplayer, o servidor é a autoridade sobre o estado do jogo
        pass
    
    

    def render(self):

        """Renderiza o jogo"""
        if self.game_state == GameState.MAIN_MENU:
            self.render_main_menu()
        elif self.game_state == GameState.SINGLEPLAYER:
            self.render_singleplayer()
        elif self.game_state == GameState.MULTIPLAYER:
            self.render_multiplayer()
        elif self.game_state == GameState.OPTIONS:
            self.render_options()
            
        pygame.display.flip()

    def render_main_menu(self):
        """Renderiza o menu principal"""
        title = self.font.render("2D Game", True, (255, 255, 255))
        singleplayer_text = self.font.render("Singleplayer (S)", True, (255, 255, 255))
        multiplayer_text = self.font.render("Multiplayer (M)", True, (255, 255, 255))
        quit_text = self.font.render("Quit (Q)", True, (255, 255, 255))
        
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        self.screen.blit(singleplayer_text, (SCREEN_WIDTH // 2 - singleplayer_text.get_width() // 2, 200))
        self.screen.blit(multiplayer_text, (SCREEN_WIDTH // 2 - multiplayer_text.get_width() // 2, 250))
        self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 300))
    
    def render_singleplayer(self):
        """Renderiza o modo singleplayer"""
        self.screen.fill((0, 100, 50))  # Cor de fundo
        # TODO: Implementar renderização do singleplayer
        self.render_game()
    
    def render_multiplayer(self):
        """Renderiza o modo multiplayer"""
        self.screen.fill((50, 50, 100))  # Cor de fundo
        # TODO: Implementar renderização do multiplayer
        self.render_game()

    def render_multiplayer_menu(self):
        """Renderiza submenu de multiplayer"""
        self.screen.fill((30, 30, 50))
        title = self.font.render("Multiplayer", True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        for i, option in enumerate(self.multiplayer_menu_options):
            color = (255, 255, 0) if i == self.multiplayer_selected else (200, 200, 200)
            text = self.font.render(option, True, color)
            y = 180 + i * 48
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y - 8, 400, 40)
            pygame.draw.rect(self.screen, (50, 50, 70), rect, border_radius=4)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))

        # Se estiver hospedando, mostra informação e IP LAN
        if self.server_hosting:
            lan_ip = self.get_local_ip()
            info = self.font.render(f"Server running. LAN IP: http://{lan_ip}:3000", True, (180, 255, 180))
            self.screen.blit(info, (20, SCREEN_HEIGHT - 40))

    
    def render_options(self):
        """Renderiza a tela de opções"""
        self.screen.fill((60, 60, 30))  # Cor de fundo
        # TODO: Implementar renderização das opções

    def render_game(self):
        """Renderiza o jogo em si"""
        # Renderiza entidades
        for entity in self.entities:
            entity.render(self.screen)
        
        # Renderiza jogadores
        if self.game_state == GameState.SINGLEPLAYER:
            if self.local_player:
                self.local_player.render(self.screen)
        else:
            for player_id, player in self.players.items():
                player.render(self.screen)
        
        # Renderiza HUD
        self.render_hud()
    
    def render_hud(self):
        """Renderiza interface do usuário"""
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            self.clock.tick(FPS)  # Controla a taxa de quadros :cite[4]
            self.handle_events()
            self.update()
            self.render()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    client = GameClient()
    client.run()