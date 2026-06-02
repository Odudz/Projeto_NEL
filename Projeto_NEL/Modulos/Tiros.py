import pygame as pg

# pygame inicialização
pg.init()

import Variaveis_Globais as vg
from Classes import Jogador, Inimigo, Projetil, ProjetilInimigo, Explosao
import utils, subprocess, sys, os, random, math

#Som tiro
som_tiro = pg.mixer.Sound(os.path.join("Sons", "tiro_som.ogg"))

#Imagens
pausado_original = pg.image.load(os.path.join("Imagens","Jogo", "Pausado.png")).convert()
pausado = pg.transform.scale(pausado_original, (1280 // 2, 720 // 2))

LARGURA = 1280
ALTURA = 720

tela = pg.display.set_mode((LARGURA, ALTURA))
pg.display.set_caption("Sistema de Tiros")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 100, 255)
AMARELO = (255, 255, 0)
CINZA = (40, 40, 40)

clock = pg.time.Clock()

fonte = pg.font.SysFont("Arial", 28)
fonte_pause = pg.font.SysFont("Arial", 60)

jogador = Jogador()

tempo_dano = 0

projeteis = []
explosoes = []
projeteis_inimigo = []

wave = 1
quantidade_inimigos = 5

inimigos = utils.Criar_Wave(Inimigo)

pause = False
gamer_over = False

rodando = True

while rodando:

    clock.tick(60)

    if not gamer_over:
        tempo_dano += 1

    for evento in pg.event.get():

        if evento.type == pg.QUIT:
            rodando = False

        if evento.type == pg.KEYDOWN:

            if evento.key == pg.K_ESCAPE and not gamer_over:
                pause = not pause

        if not pause:

            if evento.type == pg.MOUSEBUTTONDOWN:

                agora = pg.time.get_ticks()
                if agora >= vg.PROXIMO_TIRO:
                    vg.PROXIMO_TIRO = agora + jogador.stats["TAXA_ATAQUES"]

                    mx, my = pg.mouse.get_pos()

                    som_tiro.play()

                    utils.Atirar(projeteis, Projetil, jogador, mx, my)
                    vg.RAJADA += jogador.stats["QUANTIDADE_TIRO"] - 1

    tela.fill(PRETO)

    if not pause and not gamer_over:

        teclas = pg.key.get_pressed()

        x_antigo = jogador.x
        y_antigo = jogador.y

        jogador.mover(teclas)

        mx, my = pg.mouse.get_pos()
        utils.Tiros(projeteis, Projetil, jogador)

        for inimigo in inimigos:
            inimigo.mover(jogador)

            inimigo.stats["ULTIMO_TIRO"] += 1

            if inimigo.stats["ULTIMO_TIRO"] >= inimigo.stats["TAXA_ATAQUES"]:
                som_tiro.play()
                projeteis_inimigo.append( ProjetilInimigo(
                    inimigo.x,
                    inimigo.y,
                    jogador.x,
                    jogador.y,
                    inimigo.stats["DANO"],
                ))

                inimigo.stats["ULTIMO_TIRO"] = 0

        for inimigo in inimigos:

            distancia_player = math.sqrt(
                (jogador.x - inimigo.x) ** 2 +
                (jogador.y - inimigo.y) ** 2
            )

            if distancia_player < jogador.raio + inimigo.raio:

                jogador.x = x_antigo
                jogador.y = y_antigo

                if tempo_dano >= 15 and jogador.stats["VIDA_ATUAL"] > 0:

                    jogador.stats["VIDA_ATUAL"] -= inimigo.stats["DANO"]

                    if jogador.stats["VIDA_ATUAL"] < 0:
                        jogador.stats["VIDA_ATUAL"] = 0

                    tempo_dano = 0

        for projetil in projeteis[:]:

            projetil.mover()

            for inimigo in inimigos[:]:

                distancia = math.sqrt(
                    (projetil.x - inimigo.x) ** 2 +
                    (projetil.y - inimigo.y) ** 2
                )

                if distancia < projetil.raio + inimigo.raio:

                    inimigo.stats["VIDA_ATUAL"] -= jogador.stats["DANO"]

                    explosoes.append(
                        Explosao(
                            projetil.x,
                            projetil.y
                        )
                    )

                    if projetil in projeteis:
                        projeteis.remove(projetil)

                    if inimigo.stats["VIDA_ATUAL"] <= 0:
                        inimigos.remove(inimigo)
                    break

        if len(inimigos) == 0:
            utils.NovaWave(jogador)

            quantidade_inimigos += 2

            inimigos = utils.Criar_Wave(Inimigo)

        for projetil in projeteis_inimigo[:]:

            projetil.mover()

            distancia = math.sqrt(
                (projetil.x - jogador.x) ** 2 + (projetil.y - jogador.y) ** 2
            )

            if distancia < projetil.raio + jogador.raio:
                jogador.stats["VIDA_ATUAL"] -= projetil.dano

                if jogador.stats["VIDA_ATUAL"] < 0:
                    jogador.stats["VIDA_ATUAL"] = 0
                    gamer_over = True

                explosoes.append(
                    Explosao(
                        projetil.x,
                        projetil.y
                    )
                )

                projeteis_inimigo.remove(projetil)

            elif projetil.fora_da_tela():
                projeteis_inimigo.remove(projetil)


        for explosao in explosoes[:]:

            explosao.atualizar()

            if explosao.tempo <= 0:

                explosoes.remove(explosao)

        if jogador.stats["VIDA_ATUAL"] == 0:

            gamer_over = True

    jogador.desenhar()

    for inimigo in inimigos:
        inimigo.desenhar()

    for projetil in projeteis:

        projetil.desenhar()

    for projetil in projeteis_inimigo:
        projetil.desenhar()

    for explosao in explosoes:

        explosao.desenhar()

    texto = fonte.render(
        f"Quantidade de inimigos: {len(inimigos)}",
        True,
        BRANCO
    )

    tela.blit(texto, (20, 20))

    texto = fonte.render(
        f"Vida do Player: {jogador.stats["VIDA_ATUAL"]}",
        True,
        BRANCO
    )

    tela.blit(texto, (20, 60))

    texto = fonte.render(
        f"Wave: {wave}",
        True,
        BRANCO
    )

    tela.blit(texto, (20, 120))

    if pause:

        overlay = pg.Surface(
            (LARGURA, ALTURA)
        )

        overlay.set_alpha(180)

        overlay.fill(CINZA)

        tela.blit(overlay, (0, 0))

        tela.blit(pausado,(vg.LARGURA //2, 200))


        if utils.criar_botao_imagem("Voltar ao menu", vg.botao_folder, vg.LARGURA//2, 500):
            pg.quit()
            subprocess.run([sys.executable, os.path.join("Menu.py")])
            sys.exit()

        if utils.criar_botao_imagem("Continuar", vg.botao_folder, vg.LARGURA//2, 200):
            pause = not pause

    if gamer_over:

        overlay = pg.Surface((LARGURA, ALTURA))
        overlay.set_alpha(200)
        overlay.fill(CINZA)

        tela.blit(overlay, (0, 0))

        texto_morte = fonte_pause.render(
            "Você Morreu!",
            True,
            VERMELHO
        )

        tela.blit(
            texto_morte,
            (LARGURA // 2 - texto_morte.get_width() // 2,
             ALTURA // 2 - 80)
        )

        if utils.criar_botao_imagem("Voltar ao menu", vg.botao_folder, vg.LARGURA//2, 500):
            pg.quit()
            subprocess.run([sys.executable, os.path.join( "Menu.py")])
            sys.exit()

        if utils.criar_botao_imagem("Reiniciar", vg.botao_folder, vg.LARGURA // 2, 400):
            jogador = Jogador()
            wave = 1
            quantidade_inimigos = 5
            inimigos = utils.Criar_Wave(Inimigo)

            projeteis.clear()
            explosoes.clear()
            projeteis_inimigo.clear()

            tempo_dano = 0

            gamer_over = False
            pause = False

    pg.display.update()

pg.quit()