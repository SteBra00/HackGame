class Component:
    def __init__(self, name:str, type:str, power:int, life:int=100) -> None:
        self.name = name
        self.type = type
        self.power = power
        self.life = life
    
    def __str__(self) -> str:
        return f'Component: (name:{self.name}, type:{self.type}, power:{self.power}, life:{self.life})'