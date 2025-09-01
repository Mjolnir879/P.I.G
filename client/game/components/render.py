"""
Componente de renderização - gerencia a aparência visual de entidades
"""
import pygame
from typing import Optional

class RenderComponent:
    """
    Componente que adiciona capacidades de renderização a uma entidade
    Controla sprites, animações e efeitos visuais
    """
    
    def __init__(self, sprite_path: Optional[str] = None, width: int = 32, height: int = 32, color: tuple = (255, 0, 0)):
        # Caminho para o sprite (None para usar cor sólida)
        self.sprite_path = sprite_path
        # Dimensões do sprite
        self.width = width
        self.height = height
        # Cor padrão (se não houver sprite)
        self.color = color
        # Sprite carregado
        self.sprite = None
        # Frame atual da animação
        self.current_frame = 0
        # Tempo desde o último frame
        self.frame_timer = 0
        # Direção que a entidade está virada
        self.facing = "right"
        
        # Carrega o sprite se um caminho foi fornecido
        if sprite_path:
            self.load_sprite(sprite_path)
            
    def load_sprite(self, sprite_path: str) -> bool:
        """
        Carrega um sprite do disco
        sprite_path: Caminho para o arquivo de imagem
        Retorna True se o sprite foi carregado com sucesso
        """
        try:
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            return True
        except:
            print(f"Erro ao carregar sprite: {sprite_path}")
            self.sprite = None
            return False
            
    def render(self, surface: pygame.Surface, x: float, y: float) -> None:
        """
        Renderiza a entidade na superfície
        surface: Superfície onde renderizar
        x, y: Posição onde renderizar
        """
        if self.sprite:
            # Renderiza o sprite
            sprite_rect = self.sprite.get_rect()
            sprite_rect.center = (x, y)
            
            # Vira o sprite se necessário
            if self.facing == "left":
                flipped_sprite = pygame.transform.flip(self.sprite, True, False)
                surface.blit(flipped_sprite, sprite_rect)
            else:
                surface.blit(self.sprite, sprite_rect)
        else:
            # Renderiza um retângulo colorido como fallback
            rect = pygame.Rect(0, 0, self.width, self.height)
            rect.center = (x, y)
            pygame.draw.rect(surface, self.color, rect)
            
    def update_animation(self, dt: float) -> None:
        """
        Atualiza a animação
        dt: Tempo decorrido desde a última atualização
        """
        # Em uma implementação real, isso avançaria os frames de animação
        self.frame_timer += dt
        # Lógica de animação seria implementada aqui