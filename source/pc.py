from typing import List, Tuple
from source.component import *

class Pc:
    def __init__(self, name:str, *components:Tuple[int, Component]) -> None:
        self.name = name
        self.components = {c[0]:c[1] for c in components}

    def add_component(self, id:int, component:Component) -> None:
        self.components[id] = component

    def remove_component(self, id:int) -> None:
        del self.components[id]
    
    def get_life(self) -> int:
        life = 100
        for component in self.components.values():
            if component.life<life: life = component.life
        return life
    
    def get_mining_power(self) -> int:
        power = 0
        for component in self.components.values():
            if component.type=='GPU':
                power += component.power
        return power
    
    def get_component(self) -> List[Component]:
        return list(self.components.values())