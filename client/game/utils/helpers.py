"""
Funções auxiliares - diversas funções úteis para o jogo
"""
import math
import random
from typing import Tuple, List, Any

class Helpers:
    """
    Coleção de funções auxiliares para o jogo
    """
    
    @staticmethod
    def distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """
        Calcula a distância entre dois pontos
        x1, y1: Coordenadas do primeiro ponto
        x2, y2: Coordenadas do segundo ponto
        Retorna a distância entre os pontos
        """
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        """
        Interpola linearmente entre dois valores
        a: Valor inicial
        b: Valor final
        t: Fator de interpolação (0.0 a 1.0)
        Retorna o valor interpolado
        """
        return a + (b - a) * t
        
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """
        Restringe um valor dentro de um intervalo
        value: Valor a ser restringido
        min_val: Valor mínimo
        max_val: Valor máximo
        Retorna o valor restringido
        """
        return max(min_val, min(value, max_val))
        
    @staticmethod
    def random_point_in_circle(center_x: float, center_y: float, radius: float) -> Tuple[float, float]:
        """
        Gera um ponto aleatório dentro de um círculo
        center_x, center_y: Centro do círculo
        radius: Raio do círculo
        Retorna uma tupla (x, y) com as coordenadas do ponto
        """
        # Gera um ângulo aleatório
        angle = random.uniform(0, 2 * math.pi)
        # Gera um raio aleatório (usando a raiz quadrada para distribuição uniforme)
        r = radius * math.sqrt(random.uniform(0, 1))
        
        # Calcula as coordenadas
        x = center_x + r * math.cos(angle)
        y = center_y + r * math.sin(angle)
        
        return (x, y)
        
    @staticmethod
    def random_choice_weighted(items: List[Any], weights: List[float]) -> Any:
        """
        Escolhe um item aleatório com base em pesos
        items: Lista de itens
        weights: Lista de pesos (deve ter o mesmo tamanho que items)
        Retorna um item escolhido aleatoriamente
        """
        if len(items) != len(weights):
            raise ValueError("Items e weights devem ter o mesmo tamanho")
            
        # Calcula a soma total dos pesos
        total = sum(weights)
        # Gera um número aleatório entre 0 e o total
        r = random.uniform(0, total)
        
        # Percorre os itens até encontrar o escolhido
        current = 0
        for i, weight in enumerate(weights):
            current += weight
            if r <= current:
                return items[i]
                
        # Fallback (deveria nunca acontecer)
        return items[0]
        
    @staticmethod
    def format_time(seconds: float) -> str:
        """
        Formata um tempo em segundos para string MM:SS
        seconds: Tempo em segundos
        Retorna string formatada
        """
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"