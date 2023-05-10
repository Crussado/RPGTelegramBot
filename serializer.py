from game import LOSS, CATASTROFIC_LOSS, WIN, PERFECT_WIN

def serializer_stats(stats: dict) -> str:
    str = f'\t\t\- *Str*: {stats["str"]}\n'
    dex = f'\t\t\- *Dex*: {stats["dex"]}\n'
    int = f'\t\t\- *Int*: {stats["int"]}\n'
    res = f'\t\t\- *Res*: {stats["res"]}\n'
    return '\- *Stats*:\n' + str + dex + int + res

def serializer_info(info: dict) -> str:
    life = f'\- *Life*: {info["life"]}\n'
    exp = f'\- *Exp*: {info["exp"]}\n'
    gold = f'\- *Gold*: {info["gold"]}\n'
    courage = f'\- *Courage*: {info["courage"]}\n'
    stats = serializer_stats(info['stats'])
    return life + exp + gold + courage + stats
    
def serializer_enemy(enemy: dict) -> str:
    nombre = f'Enemy: {enemy["nombre"]}\n'.replace(".", "\.")
    aspecto = f'Aspecto: {enemy["aspecto"]}\n'.replace(".", "\.")
    situacion = f'{enemy["situacion"]}\n'.replace(".", "\.")
    atributo = f'Poder: {enemy["stat"]} \= {enemy["power"]}'
    return nombre + aspecto + situacion + atributo

def serializer_battle_status(status: int) -> str:
    if status == CATASTROFIC_LOSS:
        return 'Uff they destroyed you\n'
    if status == LOSS:
        return 'Damn you lost the fight\n'
    if status == WIN:
        return 'Well done my best friend, you win\n'
    if status == PERFECT_WIN:
        return 'Yeah\! you got a perfect\n'

def serializer_battle_result(data: dict) -> str:
    roll = f'*You roll*: {data["roll"]}\n'
    status = serializer_battle_status(data['status'])
    damage = f'*Damage received*: {data["damage"]}\n'
    exp = f'\-*Exp*: {data["exp"]}\n' if data["exp"] else ''
    gold = f'\-*Gold*: {data["gold"]}\n' if data["gold"] else ''
    tresure = f'Look at that is a tresure\! {data["tresure"]}\n' if data["tresure"] else ''
    return roll + status + damage + exp + gold + tresure
