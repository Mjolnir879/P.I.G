"""
Gerenciador de cenas - controla a transição entre diferentes estados do jogo
"""
from typing import Dict, Optional
from ..scenes.scene_base import SceneBase

class SceneManager:
    """
    Gerencia todas as cenas do jogo e controla as transições entre elas
    Implementa o padrão de design State para gerenciar estados do jogo
    """
    
    def __init__(self):
        # Registro de todas as cenas disponíveis
        self.scenes: Dict[str, SceneBase] = {}
        # Cena atualmente ativa
        self.current_scene: Optional[SceneBase] = None
        # Nome da cena atual (para referência)
        self.current_scene_name: Optional[str] = None
        
    def register_scene(self, scene_name: str, scene_instance: SceneBase) -> None:
        """
        Registra uma nova cena no gerenciador
        Cada cena deve ser uma instância de SceneBase ou de suas subclasses
        """
        self.scenes[scene_name] = scene_instance
        
    def switch_to(self, scene_name: str, *args, **kwargs) -> bool:
        """
        Alterna para uma cena específica
        Retorna True se a transição foi bem-sucedida, False caso contrário
        """
        if scene_name not in self.scenes:
            print(f"Erro: Cena '{scene_name}' não registrada.")
            return False
            
        # Encerra a cena atual se existir
        if self.current_scene:
            self.current_scene.exit()
            
        # Atualiza a referência para a nova cena
        self.current_scene = self.scenes[scene_name]
        self.current_scene_name = scene_name
        
        # Inicializa a nova cena
        self.current_scene.enter(*args, **kwargs)
        return True
        
    def update(self, dt: float) -> None:
        """Atualiza a cena atual"""
        if self.current_scene:
            self.current_scene.update(dt)
            
    def render(self, surface) -> None:
        """Renderiza a cena atual"""
        if self.current_scene:
            self.current_scene.render(surface)
            
    def handle_event(self, event) -> None:
        """Repassa eventos para a cena atual"""
        if self.current_scene:
            self.current_scene.handle_event(event)