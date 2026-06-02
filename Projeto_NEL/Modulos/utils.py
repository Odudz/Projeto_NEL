import random, math, time
import Variaveis_Globais as vg
import pygame as pg

#Função que calcula caso personagem crite
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

#Função que reduz a vida do personagem
def TomarDano(personagem, atacante):
    dano = CalcularDano(atacante)
    if personagem.stats and personagem.stats["VIDA_ATUAL"]:
        personagem.stats["VIDA_ATUAL"] -= dano

#Função que cura a vida do personagem
def CurarVida(personagem, vida : int):
    if personagem.stats and personagem.stats["VIDA_ATUAL"]:
        personagem.stats["VIDA_ATUAL"] = min(personagem.stats["VIDA_ATUAL"] + vida, personagem.stats["VIDA_MAXIMA"])

#Função que aumenta status do personagem
def AumentarStatus(personagem, status, quantidade):
    if personagem.stats and personagem.stats[status]:
        personagem.stats[status] += quantidade

#Status base inimigo
def StatusInimigo():
    status = {
        "VIDA_ATUAL"  : 100 + 5 * vg.ONDA,
        "VIDA_MAXIMA" : 100 + 5 * vg.ONDA,
        "DANO"        : 5 + 1 * vg.ONDA,
        "TAXA_ATAQUES": 120 - 1 * vg.ONDA,
        "ULTIMO_TIRO" : 0,
        "VELOCIDADE"  : 2 + 0.05 * vg.ONDA,
        "VELOCIDADE_TIRO": 1 + 0.25 * vg.ONDA,
    }
    return status

#Função para tiros
def Atirar(projeteis, Projetil, Jogador, Mx, My):
    if Jogador.stats["VIDA_ATUAL"] <= 0:
        return
    agora = pg.time.get_ticks()
    projeteis.append(
        Projetil(
            Jogador.x,
            Jogador.y,
            Mx,
            My,
            Jogador.stats["VELOCIDADE_TIRO"]
        )
    )
    vg.PROXIMA_RAJADA = agora + Jogador.stats["TAXA_ATAQUES"] / (1.5 * Jogador.stats["QUANTIDADE_TIRO"])
    vg.RAJADAMX, vg.RAJADAMY = Mx, My

#SubFunção para tiros
def Tiros(projeteis, Projetil, Jogador):
    if Jogador.stats["VIDA_ATUAL"] <= 0:
        return
    agora = pg.time.get_ticks()
    if vg.RAJADA > 0 and agora >= vg.PROXIMA_RAJADA:
        Atirar(projeteis, Projetil, Jogador, vg.RAJADAMX, vg.RAJADAMY)
        vg.RAJADA -= 1

#Função para aumentar a wave
def NovaWave(Jogador):
    vg.ONDA += 1
    print(f"Nova Onda! {vg.ONDA}")
    UpgradeAleatorio(Jogador)

#Função para iniciar wave nova
def Criar_Wave(Inimigo):
    lista = []

    for i in range(3 + 1 * vg.ONDA):
        lista.append(Inimigo())

    return lista

#Função de check de distância
def ChecarDistancia(Projetil, Inimigo):
    distancia = math.sqrt(
        (Projetil.x - Inimigo.x) ** 2 +
        (Projetil.y - Inimigo.y) ** 2
    )
    return distancia

#Função que aleatoriza três upgrades para o jogador
def UpgradeAleatorio(Jogador):
    upgrades = list(Jogador.stats.items())
    for i in range(3):
        aleatorio = random.choice(upgrades)
        print(f"Você pode dar upgrade no status {aleatorio}")
        upgrades.remove(aleatorio)
    pass