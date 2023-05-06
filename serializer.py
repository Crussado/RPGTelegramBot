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
    
