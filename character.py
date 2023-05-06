from random import randint
from settings import STATS

INITIAL_LIFE = 100
LIFE_FACTOR = 1.05
LIMIT_EXP = 100
GOLD_FOR_LVL = 10

class Character:
    def __init__(self, name : str, clas : str, race : str) -> None:
        self.exp : int = 0
        self.gold : int = 0
        self.lvl : int = 1
        self._max_life : int = INITIAL_LIFE
        self.life : int = self._max_life
        self.name : str = name
        self.clas : str = clas
        self.race : str = race
        self.stats : dict = { stat: randint(1, 20) for stat in STATS }

    def __str__(self) -> str:
        return f'{ self.name } - { self.clas } - { self.race }'

    def _lvl_up(self) -> None:
        self.lvl += 1
        self._max_life *= LIFE_FACTOR
        self.life = self._max_life

    def add_exp(self, exp : int) -> bool:
        self.exp += exp
        if self.exp >= LIMIT_EXP:
            self.exp -= LIMIT_EXP
            self._lvl_up()
            return True
        return False
    
    def add_stat(self, stat : str) -> None:
        self.stats[stat] += 1
    
    def add_gold(self, gold : int) -> None:
        self.gold += gold

    def add_damage(self, damage : int) -> None:
        self.life -= damage
    
    def gold_for_lvl(self) -> None:
        if self.gold >= GOLD_FOR_LVL:
            self.gold = 0
            self._lvl_up()
