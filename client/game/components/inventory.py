"""
Componente de inventário - gerencia itens e equipamentos de entidades
"""
from typing import Dict, List, Optional

class InventoryComponent:
    """
    Componente que adiciona sistema de inventário a uma entidade
    Permite coletar, armazenar e usar itens
    """
    
    def __init__(self, capacity: int = 20):
        # Capacidade máxima do inventário
        self.capacity = capacity
        # Itens no inventário (nome -> quantidade)
        self.items: Dict[str, int] = {}
        # Itens equipados (slot -> item)
        self.equipped: Dict[str, str] = {}
        # Moedas/ouro
        self.gold = 0
        
    def add_item(self, item_name: str, quantity: int = 1) -> bool:
        """
        Adiciona um item ao inventário
        item_name: Nome do item
        quantity: Quantidade a adicionar
        Retorna True se o item foi adicionado, False se não há espaço
        """
        # Verifica se há espaço no inventário
        if self.get_total_items() + quantity > self.capacity:
            return False
            
        # Adiciona o item
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
            
        return True
        
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """
        Remove um item do inventário
        item_name: Nome do item
        quantity: Quantidade a remover
        Retorna True se o item foi removido, False se não havia quantidade suficiente
        """
        if item_name not in self.items or self.items[item_name] < quantity:
            return False
            
        self.items[item_name] -= quantity
        
        # Remove o item do dicionário se a quantidade chegar a zero
        if self.items[item_name] == 0:
            del self.items[item_name]
            
        return True
        
    def get_total_items(self) -> int:
        """
        Retorna o número total de itens no inventário
        """
        return sum(self.items.values())
        
    def equip_item(self, slot: str, item_name: str) -> bool:
        """
        Equipa um item em um slot específico
        slot: Nome do slot (ex: "mão_esquerda", "mão_direita")
        item_name: Nome do item a equipar
        Retorna True se o item foi equipado, False se o item não existe
        """
        if item_name not in self.items:
            return False
            
        # Equipa o item
        self.equipped[slot] = item_name
        return True
        
    def unequip_item(self, slot: str) -> Optional[str]:
        """
        Desequipa um item de um slot
        slot: Nome do slot
        Retorna o nome do item que estava equipado, ou None se o slot estava vazio
        """
        return self.equipped.pop(slot, None)
        
    def has_item(self, item_name: str, quantity: int = 1) -> bool:
        """
        Verifica se a entidade possui uma quantidade específica de um item
        item_name: Nome do item
        quantity: Quantidade a verificar
        Retorna True se possui a quantidade especificada
        """
        return item_name in self.items and self.items[item_name] >= quantity