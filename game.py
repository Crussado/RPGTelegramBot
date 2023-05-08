from random import randint
import openai
from typing import Union

from character import Character
from settings import API_KEY, ENEMY_KEYS

CATASTROFIC_LOSS, LOSS, WIN, PERFECT_WIN = range(4)

INITIAL_CHAT = """A partir de ahora quiero que generes enemigos de un juego d&d que tendran 5 caracteristicas el nombre, aspecto, una situacion con la que el heroe se encontrara con el, en que atributo es fuerte el enemigo, los atributos pueden ser [dex, str, int, res], el nombre de un "tesoro" que el jugador obtendra por vencer el enemigo, el nivel de poder del enemigo, este ultimo debe ser un numero del 1 al 20.  La informacion debe ser un json.
Quiero que los enemigos sean bizarros, chistosos, y grotescos, ejemplos: pato mutante, zombie panadero, necro-araña mutante ecologista.
Yo te los ire pidiendo y solo quiero que respondas con el json."""

class StateGame:
    def __init__(self, name : str, clas: str, race: str) -> None:
        self.treasures : list[str] = []
        self.heroe : Character = Character(name, clas, race)
        self.courage : int = 0
        self.actual_enemy : dict = {}
        openai.api_key = API_KEY

    def get_info_heroe(self):
        return {
            'life': self.heroe.life,
            'exp': self.heroe.exp,
            'gold': self.heroe.gold,
            'courage': self.courage,
            'stats': self.heroe.stats,
        }

    def heroe_win(self) -> bool:
        return self.heroe.lvl >= 10 and self.heroe.life > 0
    
    def heroe_loss(self) -> bool:
        return self.heroe.life <= 0

    def _parser_response_gpt(self, response: str) -> Union[dict, bool]:
        inicio = response.find('{')
        fin = response.find('}')
        if inicio != -1 and fin != -1:
            dict_str = response[inicio:fin+1].strip()
            enemy = eval(dict_str)
            for key in ENEMY_KEYS:
                if not key in enemy:
                    return False
            return enemy
        return False

    def generate_battle(self) -> dict:
        enemy = False
        while not enemy:
            completion: openai.ChatCompletion = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'system', 'content': INITIAL_CHAT}, {'role': 'user', 'content': 'Genera un enemigo'}]
            )
            response: str = completion.choices[0]['message']['content']
            enemy = self._parser_response_gpt(response)

        self.actual_enemy = enemy
        return self.actual_enemy

    def pass_battle(self) -> None:
        self.courage -= 2

    def _loss_battle(self, catastrofic: bool) -> dict:
        if catastrofic:
            damage: int = randint(10, 20)
        else:
            damage: int = randint(1, 20)

        self.heroe.add_damage(damage)
        self.courage -= 1

        return {
            'damage': damage,
        }

    def _win_battle(self, perfect: bool) -> dict:
        if perfect:
            damage: int = 0
        else:
            damage: int = randint(1, 10)

        self.heroe.add_damage(damage)
        exp: int = randint(1, 20)
        self.heroe.add_exp(exp)
        gold: int = randint(1, 20)
        self.gold += gold
        self.courage += 1
        self.treasures += self.actual_enemy['tesoro']

        return {
            'damage': damage,
            'exp': exp,
            'gold': gold,
            'tresure': self.actual_enemy['tesoro']
        }

    def fight_battle(self) -> int:
        roll: int = randint(1, 20)
        stat: int = self.heroe.stats[self.actual_enemy['atributo_fuerte']] + roll

        if stat <= self.actual_enemy['nivel_poder'] - 5:
            data =self._loss_battle(True)
            data['status'] = CATASTROFIC_LOSS
        elif stat <= self.actual_enemy['nivel_poder'] + 3:
            data = self._loss_battle(False)
            data['status'] = LOSS
        elif stat >= self.actual_enemy['nivel_poder'] + 10:
            data = self._win_battle(True)
            data['status'] = PERFECT_WIN
        else:
            data = self._win_battle(False)
            data['status'] = WIN

        data['roll'] = roll
        return data
        
    def get_score(self) -> int:
        return self.heroe.lvl + len(self.treasures) + 0.1 (self.heroe.exp + self.heroe.gold + self.heroe.life)

    def pay_for_lvl(self):
        pass