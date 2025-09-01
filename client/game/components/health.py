"""
Componente de saúde - gerencia pontos de vida, dano e cura de entidades
"""
class HealthComponent:
    """
    Componente que adiciona sistema de saúde a uma entidade
    Permite que entidades recebam dano, sejam curadas e morram
    """
    
    def __init__(self, max_health: int = 100):
        # Saúde máxima da entidade
        self.max_health = max_health
        # Saúde atual
        self.current_health = max_health
        # Flag indicando se a entidade está morta
        self.is_dead = False
        
    def take_damage(self, amount: int) -> None:
        """
        Aplica dano à entidade
        amount: Quantidade de dano a ser aplicada
        """
        if self.is_dead:
            return  # Entidades mortas não podem receber dano
            
        # Reduz a saúde atual
        self.current_health -= amount
        
        # Verifica se a entidade morreu
        if self.current_health <= 0:
            self.current_health = 0
            self.is_dead = True
            print("Entidade morreu!")
            
    def heal(self, amount: int) -> None:
        """
        Cura a entidade
        amount: Quantidade de saúde a ser recuperada
        """
        if self.is_dead:
            return  # Entidades mortas não podem ser curadas
            
        # Aumenta a saúde atual, sem ultrapassar o máximo
        self.current_health = min(self.current_health + amount, self.max_health)
        
    def get_health_percentage(self) -> float:
        """
        Retorna a porcentagem de saúde atual (0.0 a 1.0)
        """
        return self.current_health / self.max_health
        
    def respawn(self) -> None:
        """Ressuscita a entidade e restaura sua saúde"""
        self.current_health = self.max_health
        self.is_dead = False