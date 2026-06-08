import random, math, time, os
import Variaveis_Globais as vg
import pygame as pg

ultimo_clique = 0

imagem_melhoria_original = pg.image.load(
    os.path.join("Imagens", "Menu", "melhoria.png")
)

imagem_melhoria = pg.transform.scale(
    imagem_melhoria_original,
    (vg.LARGURA // 3, vg.ALTURA // 3)
)

def CalcularDano(personagem):
    """
    Função que calcula caso personagem crite
    :param personagem: Personagem Atual
    :return: Dano ou 10
    """
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
    """
    Função que reduz a vida do personagem
    :param personagem: Personagem Atual
    :param atacante: Atacante do personagem
    :return: None
    """
    dano = CalcularDano(atacante)
    if personagem.stats and personagem.stats["VIDA_ATUAL"]:
        personagem.stats["VIDA_ATUAL"] -= dano

def CurarVida(vida : int):
    """
    Função que cura a vida do personagem
    :param vida: Vida a ser curada
    :return: None
    """
    Jogador = vg.Jogador
    if Jogador.stats and Jogador.stats["VIDA_ATUAL"]:
        Jogador.stats["VIDA_ATUAL"] = min(Jogador.stats["VIDA_ATUAL"] + vida, Jogador.stats["VIDA_MAXIMA"])

def AumentarStatus(status, quantidade):
    """
    Função que aumenta status do personagem
    :param status: Status a ser melhorado
    :param quantidade: Quantidade a ser aumentada
    :return: None
    """
    Jogador = vg.Jogador
    if Jogador.stats and Jogador.stats[status]:
        Jogador.stats[status] += quantidade

def randomClass(status):
    """
    Seleciona uma classe aleatória para o inimigo
    :param status: Status atual do inimigo
    :return: Classe aleatória
    """
    num = random.randint(1,3)
    if num == 1: # Mercenário
        status["DANO"]            = 3 + 1 * vg.ONDA
        status["VELOCIDADE"]      = 3 + 0.15 * vg.ONDA
        status["VELOCIDADE_TIRO"] = 1.5 + 0.25 * vg.ONDA
        status["COLOR"]           = vg.VERDE
    elif num == 2: # Atirador
        status["DANO"]            = 5 + 2 * vg.ONDA
        status["VELOCIDADE_TIRO"] = 10 + .5 * vg.ONDA
        status["VELOCIDADE"]      = 0 + 0 * vg.ONDA
        status["COLOR"]           = vg.AMARELO
    elif num == 3: #Tanque
        status["VIDA_ATUAL"]  = 50 + 5 * vg.ONDA
        status["VIDA_MAXIMA"] = 50 + 5 * vg.ONDA
        status["VELOCIDADE"]  = 1 + 0.05 * vg.ONDA
        status["COLOR"]       = vg.ROXO
    return status

def randomClassChefe(status):
    """
    Seleciona uma classe aleatória para o inimigo
    :param status: Status atual do inimigo
    :return: Classe aleatória
    """
    num = random.randint(1,3)
    if num == 1: # Mercenário
        status["DANO"]            = 10
        status["VELOCIDADE"]      = 0
        status["VELOCIDADE_TIRO"] = 0
        status["COLOR"]           = vg.VERDE
    elif num == 2: # Atirador
        status["DANO"]            = 20
        status["VELOCIDADE_TIRO"] = 20
        status["VELOCIDADE"]      = 0 + 0 * vg.ONDA
        status["COLOR"]           = vg.AMARELO
    elif num == 3: #Tanque
        status["VIDA_ATUAL"]  = 750
        status["VIDA_MAXIMA"] = 750
        status["VELOCIDADE"]  = 0
        status["COLOR"]       = vg.ROXO
    return status

def StatusInimigo():
    """
    Status base inimigo
    :return: Status do inimigo como dicionário
    """
    status = {
        "VIDA_ATUAL"  : 15 + 5 * vg.ONDA,
        "VIDA_MAXIMA" : 15 + 5 * vg.ONDA,
        "DANO"        : 2 + 1 * vg.ONDA,
        "TAXA_ATAQUES": 160 - 2 * vg.ONDA,
        "ULTIMO_TIRO" : 0,
        "VELOCIDADE"  : 2 + 0.05 * vg.ONDA,
        "VELOCIDADE_TIRO": 3 + 0.5 * vg.ONDA,
    }
    status = randomClass(status)
    return status

def StatusChefe():
    """
    Status base Chefão
    :return: Status do Chefão como dicionário
    """
    status = {
        "VIDA_ATUAL"  : 300,
        "VIDA_MAXIMA" : 300,
        "DANO"        : 20,
        "TAXA_ATAQUES": 100,
        "ULTIMO_TIRO" : 0,
        "VELOCIDADE"  : 0,
        "VELOCIDADE_TIRO": 10,
    }
    status = randomClassChefe(status)
    return status

def Atirar(projeteis, Projetil, Mx, My):
    """
    Função para tiros
    :param projeteis: Lista de projeteis
    :param Projetil: Projetil atual
    :param Jogador: Jogador Atual
    :param Mx: Posição X do mouse
    :param My: Posição Y do mouse
    :return: None
    """
    Jogador = vg.Jogador
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

def Tiros(projeteis, Projetil):
    """
    SubFunção para tiros
    :param projeteis: Lista de projeteis
    :param Projetil: Projetil atual
    :return: None
    """
    Jogador = vg.Jogador
    if Jogador.stats["VIDA_ATUAL"] <= 0:
        return
    agora = pg.time.get_ticks()
    if vg.RAJADA > 0 and agora >= vg.PROXIMA_RAJADA:
        Atirar(projeteis, Projetil, vg.RAJADAMX, vg.RAJADAMY)
        vg.RAJADA -= 1

def NovaWave():
    """
    Função para aumentar a wave
    :param Jogador: Jogador para função de upgrade
    :return: None
    """
    vg.ONDA += 1

    vg.MENU_MELHORIA = True

    print(f"Nova Onda! {vg.ONDA}")

def Spawn_Boss():
    import Chefão
    chefe = Chefão.Chefao()
    return [chefe]

def Criar_Wave(Inimigo):
    """
    Função para iniciar wave nova
    :param Inimigo: Inimigo que deve ser replicado na nova wave
    :return: lista de inimigos
    """
    lista = []

    if vg.ONDA == 10:
        return Spawn_Boss()

    for i in range(3 + 1 * vg.ONDA):
        lista.append(Inimigo())

    return lista

def ChecarDistancia(Projetil, Inimigo):
    """
    Função de check de distância
    :param Projetil: Projétil inimigo para calcular a distância
    :param Inimigo: Inimigo para calcular a distância
    :return: distância entre ambas as partes
    """
    distancia = math.sqrt(
        (Projetil.x - Inimigo.x) ** 2 +
        (Projetil.y - Inimigo.y) ** 2
    )
    return distancia

def UpgradeAleatorio():
    """
    Função que aleatoriza três upgrades para o jogador
    :param Jogador: Retorna o personagem do jogador
    :return: none
    """
    Jogador = vg.Jogador
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

    botao = imagem.get_rect(center=(x, y))

    botao_menor = botao.inflate(-100, -50)

    agora = pg.time.get_ticks()

    clicou = False

    if botao_menor.collidepoint(mouse):

        if clique[0] and agora - ultimo_clique > 300:

            ultimo_clique = agora

            clicou = True

    # desenha imagem
    vg.tela.blit(imagem, botao)

    # texto
    texto_render = vg.fonte.render(
        texto,
        True,
        vg.BRANCO
    )

    texto_rect = texto_render.get_rect(
        center=botao.center
    )

    vg.tela.blit(texto_render, texto_rect)

    return clicou

def melhorias():
    Jogador = vg.Jogador
    if not vg.MENU_MELHORIA:
        return

    # cria melhorias apenas uma vez
    if not hasattr(vg, "MELHORIAS_ATUAIS"):

        vg.MELHORIAS_ATUAIS = [
                "VIDA ATUAL",
                "VIDA MAXIMA" ,
                "DANO",
                "TAXA ATAQUES",
                "VELOCIDADE",
                "VELOCIDADE TIRO",
                "QUANTIDADE TIRO"
            ]

    overlay = pg.Surface(
        (vg.LARGURA, vg.ALTURA)
    )

    overlay.set_alpha(180)

    overlay.fill(vg.CINZA)

    vg.tela.blit(overlay, (0, 0))

    titulo = vg.fonte.render(
        "Escolha uma melhoria",
        True,
        vg.BRANCO
    )

    titulo_rect = titulo.get_rect(
        center=(vg.LARGURA // 2, 100)
    )

    vg.tela.blit(titulo, titulo_rect)

    posicoes = [

        (vg.LARGURA // 4, vg.ALTURA // 2),

        (vg.LARGURA // 2, vg.ALTURA // 2),

        (3 * vg.LARGURA // 4, vg.ALTURA // 2)

    ]

    for i in range(3):

        aleatorio = vg.UpgradeAleatorio[i]
        if vg.UpgradeAleatorio[i] == "Nenhum":

            aleatorio = random.randint(0, len(vg.MELHORIAS_ATUAIS) - 1)
            vg.UpgradeAleatorio[i] = aleatorio
            return

        melhoria = vg.MELHORIAS_ATUAIS[aleatorio]

        texto_upgrade = f"+25% {melhoria.lower()}"

        if criar_botao_imagem(
            texto_upgrade,
            imagem_melhoria,
            posicoes[i][0],
            posicoes[i][1]
        ):

            if melhoria == "DANO":
                Jogador.stats["DANO"] *= 1.25

            elif melhoria == "VIDA MAXIMA":
                Jogador.stats["VIDA_MAXIMA"] *= 1.25
                Jogador.stats["VIDA_ATUAL"] *= 1.25

            elif melhoria == "VELOCIDADE":
                Jogador.stats["VELOCIDADE"] *= 1.15
                Jogador.vel = Jogador.stats["VELOCIDADE"]

            elif melhoria == "VELOCIDADE TIRO":
                Jogador.stats["VELOCIDADE_TIRO"] *= 1.25

            elif melhoria == "CHANCE CRITICO":
                Jogador.stats["CHANCE_CRITICO"] += 5

            elif melhoria == "DANO CRITICO":
                Jogador.stats["DANO_CRITICO"] += 0.5

            elif melhoria == "QUANTIDADE TIRO":
                Jogador.stats["QUANTIDADE_TIRO"] += 1

            elif melhoria == "TAXA ATAQUES":
                Jogador.stats["TAXA_ATAQUES"] *= 0.85

            # fecha menu
            vg.MENU_MELHORIA = False
            vg.ESCOLHENDO_MELHORIA = False
            vg.UpgradeAleatorio[i] = "Nenhum"

    pg.display.update()

def SpawnAleatorio():
    while True:
        x = random.randint(20, 1000)
        y = random.randint(20, 700)

        distancia = math.sqrt(
            (x - vg.Jogador.x) ** 2 +
            (y - vg.Jogador.y) ** 2
        )

        if distancia >= 350:
            break
    return x, y