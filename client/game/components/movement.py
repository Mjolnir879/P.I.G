"""
Componente de movimento - gerencia posição, velocidade e física de entidades
"""
class MovementComponent:
    """
    Componente que adiciona movimento e física a uma entidade
    Controla posição, velocidade, aceleração e colisões
    """
    
    def __init__(self, x: float, y: float, speed: float = 5.0):
        # Posição atual
        self.x = x
        self.y = y
        # Velocidade base
        self.speed = speed
        # Velocidade atual
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        # Aceleração (para movimento suave)
        self.acceleration = 0.5
        # Desaceleração (atrito)
        self.deceleration = 0.8
        
    def update(self, dt: float) -> None:
        """
        Atualiza a posição baseada na velocidade
        dt: Tempo decorrido desde a última atualização (em segundos)
        """
        # Aplica aceleração e deceleração para suavizar o movimento
        if self.velocity_x != 0 or self.velocity_y != 0:
            # Move a entidade
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt
            
            # Aplica desaceleração
            self.velocity_x *= self.deceleration
            self.velocity_y *= self.deceleration
            
            # Se a velocidade for muito pequena, para completamente
            if abs(self.velocity_x) < 0.1:
                self.velocity_x = 0
            if abs(self.velocity_y) < 0.1:
                self.velocity_y = 0
                
    def move(self, direction_x: float, direction_y: float) -> None:
        """
        Define a velocidade baseada em uma direção
        direction_x: Direção no eixo X (-1 a 1)
        direction_y: Direção no eixo Y (-1 a 1)
        """
        # Normaliza a direção para movimento diagonal não ser mais rápido
        if direction_x != 0 and direction_y != 0:
            direction_x *= 0.7071  # √2/2
            direction_y *= 0.7071
            
        # Define a velocidade
        self.velocity_x = direction_x * self.speed
        self.velocity_y = direction_y * self.speed
        
    def stop(self) -> None:
        """Para imediatamente o movimento"""
        self.velocity_x = 0
        self.velocity_y = 0
        
    def get_position(self) -> tuple:
        """Retorna a posição atual"""
        return (self.x, self.y)
        
    def set_position(self, x: float, y: float) -> None:
        """Define a posição atual"""
        self.x = x
        self.y = y