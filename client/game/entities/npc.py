"""
Implementação de NPCs (Personagens Não-Jogáveis) - entidades com diálogo e interação
"""
from ..core.entity_system import EntitySystem
from ..components.movement import MovementComponent
from ..ai.ai_controller import AIController

class NPC:
    """
    Representa um NPC (Personagem Não-Jogável) no jogo
    Pode ter diálogo, missões ou outras interações com o jogador
    """
    
    def __init__(self, entity_system: EntitySystem, x: float, y: float, npc_type: str, dialogue_tree: dict):
        """
        Inicializa um novo NPC
        entity_system: Referência ao sistema de entidades
        x, y: Posição inicial do NPC
        npc_type: Tipo do NPC (mercador, quest giver, etc.)
        dialogue_tree: Árvore de diálogo para interação com o jogador
        """
        # Cria uma nova entidade no sistema
        self.entity_id = entity_system.create_entity()
        self.entity_system = entity_system
        self.npc_type = npc_type
        self.dialogue_tree = dialogue_tree
        
        # Adiciona componentes ao NPC
        entity_system.add_component(self.entity_id, MovementComponent(x, y, 1.0))
        
        # Adiciona controlador de IA para movimento básico
        entity_system.add_component(self.entity_id, AIController())
        
        # Marca como NPC no sistema de tags
        entity_system.add_tag(self.entity_id, "npc")
        entity_system.add_tag(self.entity_id, npc_type)  # Tag específica por tipo
        
    def interact(self, player_id: str) -> dict:
        """
        Inicia interação com o jogador
        Retorna o diálogo inicial baseado na árvore de diálogo
        """
        return self.dialogue_tree.get("initial", {"text": "Olá, viajante!"})
        
    def handle_dialogue_choice(self, choice_index: int) -> dict:
        """
        Processa uma escolha de diálogo feita pelo jogador
        Retorna a próxima fala baseada na escolha
        """
        current_dialogue = self.dialogue_tree.get("initial", {})
        choices = current_dialogue.get("choices", [])
        
        if 0 <= choice_index < len(choices):
            next_node = choices[choice_index].get("next")
            return self.dialogue_tree.get(next_node, {"text": "Obrigado pela conversa!"})
            
        return {"text": "Não entendi o que você quis dizer."}