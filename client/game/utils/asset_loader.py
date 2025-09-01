"""
Carregador de assets - gerencia o carregamento e cache de recursos
"""
import pygame
import os
from typing import Dict, Any

class AssetLoader:
    """
    Utilitário para carregar e gerenciar assets do jogo (imagens, sons, fontes)
    Implementa cache para evitar carregar o mesmo asset múltiplas vezes
    """
    
    def __init__(self):
        # Cache de imagens
        self.images: Dict[str, pygame.Surface] = {}
        # Cache de sons
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        # Cache de fontes
        self.fonts: Dict[str, Dict[int, pygame.font.Font]] = {}
        
    def load_image(self, file_path: str, alpha: bool = True) -> pygame.Surface:
        """
        Carrega uma imagem do disco (com cache)
        file_path: Caminho para o arquivo de imagem
        alpha: Se True, converte a imagem para usar canal alfa
        Retorna a superfície da imagem
        """
        # Verifica se a imagem já está em cache
        if file_path in self.images:
            return self.images[file_path]
            
        # Carrega a imagem
        try:
            if alpha:
                image = pygame.image.load(file_path).convert_alpha()
            else:
                image = pygame.image.load(file_path).convert()
                
            # Armazena no cache
            self.images[file_path] = image
            return image
            
        except Exception as e:
            print(f"Erro ao carregar imagem {file_path}: {e}")
            # Retorna uma imagem de fallback
            return self.create_fallback_image()
            
    def load_sound(self, file_path: str) -> pygame.mixer.Sound:
        """
        Carrega um som do disco (com cache)
        file_path: Caminho para o arquivo de som
        Retorna o objeto de som
        """
        # Verifica se o som já está em cache
        if file_path in self.sounds:
            return self.sounds[file_path]
            
        # Carrega o som
        try:
            sound = pygame.mixer.Sound(file_path)
            self.sounds[file_path] = sound
            return sound
            
        except Exception as e:
            print(f"Erro ao carregar som {file_path}: {e}")
            # Retorna um som vazio de fallback
            return pygame.mixer.Sound(buffer=bytearray())
            
    def load_font(self, file_path: str, size: int) -> pygame.font.Font:
        """
        Carrega uma fonte do disco (com cache)
        file_path: Caminho para o arquivo de fonte
        size: Tamanho da fonte
        Retorna o objeto de fonte
        """
        # Verifica se a fonte já está em cache
        if file_path in self.fonts and size in self.fonts[file_path]:
            return self.fonts[file_path][size]
            
        # Carrega a fonte
        try:
            font = pygame.font.Font(file_path, size)
            
            # Inicializa o dicionário para esta fonte se necessário
            if file_path not in self.fonts:
                self.fonts[file_path] = {}
                
            self.fonts[file_path][size] = font
            return font
            
        except Exception as e:
            print(f"Erro ao carregar fonte {file_path}: {e}")
            # Retorna uma fonte padrão
            return pygame.font.SysFont("Arial", size)
            
    def create_fallback_image(self) -> pygame.Surface:
        """
        Cria uma imagem de fallback (quadrado roxo com X vermelho)
        Útil quando uma imagem não pode ser carregada
        """
        surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        surface.fill((255, 0, 255))  # Rosa choque
        pygame.draw.line(surface, (255, 0, 0), (0, 0), (32, 32), 2)
        pygame.draw.line(surface, (255, 0, 0), (32, 0), (0, 32), 2)
        return surface
        
    def clear_cache(self) -> None:
        """Limpa o cache de assets"""
        self.images.clear()
        self.sounds.clear()
        self.fonts.clear()