from character import Character

class StateGame:
    def __init__(self, character : Character) -> None:
        self.treasures : list[str] = []
        self.heroe : Character = character
        self.courage : int = 0
        self.actual_enemy : dict = {}

    def get_info_heroe(self):
        return {
            'life': self.heroe.life,
            'exp': self.heroe.exp,
            'gold': self.heroe.gold,
            'stats': self.heroe.stats,
        }

    def heroe_win(self) -> bool:
        return self.heroe.lvl >= 10 and self.heroe.life > 0
    
    def heroe_loss(self) -> bool:
        return self.heroe.life <= 0
    
    def generate_battle(self) -> dict: # TODO
        pass

    def pass_battle(self) -> None:
        self.courage -= 2

    def _loss_battle(self) -> None: # TODO: ADD CATASTROFIC LOSS
        damage = 0 # TODO: CALCULATE
        self.heroe.add_damage(damage)
        self.courage -= 1

    def _win_battle(self) -> None: # TODO: ADD PERFECT WIN
        exp = 0 # TODO: CALCULATE
        self.heroe.add_exp(exp)
        self.courage += 1

    def fight(self) -> bool:
        roll = 5 # TODO: GENERATE ROLL
        stat = self.heroe.stats[self.actual_enemy['stat']] + roll
        win = stat >= 10
        if win:
            self._win_battle()
        else:
            self._loss_battle()
        return win

    def get_score(self) -> int:
        return self.heroe.lvl + len(self.treasures) + 0.1 (self.heroe.exp + self.heroe.gold + self.heroe.life)
