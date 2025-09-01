"""
Módulo de componentes - define os componentes reutilizáveis para o sistema ECS
"""
# Expõe todos os componentes disponíveis
from .health import HealthComponent
from .inventory import InventoryComponent
from .movement import MovementComponent
from .combat import CombatComponent
from .render import RenderComponent