"""
Cena do menu principal - primeira tela vista pelo jogador
"""
import pygame
from .scene_base import SceneBase

class MainMenu(SceneBase):
    """
    Menu principal do jogo
    Permite escolher entre singleplayer, multiplayer e sair do jogo
    """
    
    def __init__(self, game):
        super().__init__(game)
        # Opções do menu
        self.options = ["Singleplayer", "Multiplayer", "Options", "Quit"]
        # Índice da opção selecionada
        self.selected_option = 0
        # Fonte para renderizar texto
        self.font = pygame.font.SysFont("Arial", 36)
        
    def enter(self, *args, **kwargs):
        """Inicializa o menu principal"""
        print("Entrando no menu principal")
        
    def exit(self):
        """Limpa recursos do menu principal"""
        print("Saindo do menu principal")
        
    def update(self, dt: float):
        """Atualiza a lógica do menu"""
        # Menu principal não precisa de atualizações complexas
        pass
        
    def render(self, surface: pygame.Surface):
        """Renderiza o menu na tela"""
        # Preenche o fundo com uma cor
        surface.fill((30, 30, 60))
        
        # Renderiza o título do jogo
        title_font = pygame.font.SysFont("Arial", 48)
        title_text = title_font.render("Meu Jogo RPG", True, (255, 255, 255))
        surface.blit(title_text, (surface.get_width() // 2 - title_text.get_width() // 2, 100))
        
        # Renderiza cada opção do menu
        for i, option in enumerate(self.options):
            # Destaque a opção selecionada
            color = (255, 255, 0) if i == self.selected_option else (200, 200, 200)
            option_text = self.font.render(option, True, color)
            surface.blit(option_text, (surface.get_width() // 2 - option_text.get_width() // 2, 200 + i * 50))
            
    def handle_event(self, event: pygame.event.Event):
        """Processa eventos de entrada no menu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Move seleção para cima
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                # Move seleção para baixo
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                # Processa a opção selecionada
                self.process_selection()
                
    def process_selection(self):
        """Processa a opção selecionada no menu"""
        option = self.options[self.selected_option]
        
        if option == "Singleplayer":
            # Inicia jogo singleplayer
            self.game.scene_manager.switch_to("game_world", is_multiplayer=False)
        elif option == "Multiplayer":
            # Vai para o lobby multiplayer
            self.game.scene_manager.switch_to("multiplayer_lobby")
        elif option == "Options":
            # Abre menu de opções (não implementado)
            print("Abrindo opções...")
        elif option == "Quit":
            # Sai do jogo
            self.game.running = False