import pygame as pg

# pygame inicialização
pg.init()

import random, math
import Variaveis_Globais as vg

ultimo_clique = 0

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

def Atirar(projeteis, Projetil, Jogador, Mx, My):
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

def Tiros(projeteis, Projetil, Jogador):
    agora = pg.time.get_ticks()
    if vg.RAJADA > 0 and agora >= vg.PROXIMA_RAJADA:
        Atirar(projeteis, Projetil, Jogador, vg.RAJADAMX, vg.RAJADAMY)
        vg.RAJADA -= 1

def NovaWave(Jogador):
    vg.ONDA += 1
    print(f"Nova Onda! {vg.ONDA}")
    UpgradeAleatorio(Jogador)

def Criar_Wave(Inimigo):
    lista = []

    for i in range(5 + 2 * vg.ONDA):
        lista.append(Inimigo())

    return lista

def ChecarDistancia(Projetil, Inimigo):
    distancia = math.sqrt(
        (Projetil.x - Inimigo.x) ** 2 +
        (Projetil.y - Inimigo.y) ** 2
    )
    return distancia

def UpgradeAleatorio(Jogador):
    upgrades = list(Jogador.stats.items())
    for i in range(3):
        aleatorio = random.choice(upgrades)
        print(f"Você pode dar upgrade no status {aleatorio}")
        upgrades.remove(aleatorio)
    pass

def criar_botao_imagem(texto, imagem, x, y):
    global ultimo_clique

    mouse = pg.mouse.get_pos()
    clique = pg.mouse.get_pressed()

    # Cria o retângulo com base na posição (x, y) e tamanho da imagem
    botao = imagem.get_rect(center=(x,y))
    botao_menor = botao.inflate(-100, -50)

    agora = pg.time.get_ticks()
    clicou = False

    if botao_menor.collidepoint(mouse):
        # Verifica clique + cooldown
        if clique[0] and agora - ultimo_clique > 1000:
            ultimo_clique = agora
            clicou = True

    # 1. Desenha a imagem do botão na tela
    vg.tela.blit(imagem, botao)


    # 2. Renderiza e centraliza o texto por cima da imagem
    texto_render = vg.fonte.render(texto, True, vg.BRANCO)
    texto_rect = texto_render.get_rect(center=botao.center)
    vg.tela.blit(texto_render, texto_rect)

    return clicou

