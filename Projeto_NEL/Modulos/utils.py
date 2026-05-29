import random

def CalcularDano(personagem):
    if personagem.stats and personagem.stats["DANO"]:
        crit = random.randint(0,100)
        dano = personagem.stats["DANO"]
        chance_critico = personagem.stats["CHANCE_CRITICO"]
        if crit < chance_critico:
            print("Critico")
            dano *= personagem.stats["DANO_CRITICO"]
        return dano
    return 10

def TomarDano(personagem, atacante):
    dano = CalcularDano(atacante)
    if personagem.stats and personagem.stats["VIDA_ATUAL"]:
        personagem.stats["VIDA_ATUAL"] -= dano

def CurarVida(personagem, vida : int):
    if personagem.stats and personagem.stats["VIDA_ATUAL"]:
        personagem.stats["VIDA_ATUAL"] = min(personagem.stats["VIDA_ATUAL"] + vida, personagem.stats["VIDA_MAXIMA"])

def AumentarStatus(personagem, status, quantidade):
    if personagem.stats and personagem.stats[status]:
        personagem.stats[status] += quantidade