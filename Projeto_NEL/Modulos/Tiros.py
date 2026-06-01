import pygame as pg
import Variaveis_Globais as vg
from Classes import Jogador, Inimigo, Projetil, Explosao
import utils,math, subprocess, sys, os

pg.init()

#Som tiro
som_tiro = pg.mixer.Sound(os.path.join("..",vg.SONS, "tiro_som.ogg"))

tela = pg.display.set_mode((vg.LARGURA, vg.ALTURA))
pg.display.set_caption("Sistema de Tiros")

clock = pg.time.Clock()

fonte = pg.font.SysFont("Arial", 28)
fonte_pause = pg.font.SysFont("Arial", 60)

jogador = Jogador()
inimigo = Inimigo()

projeteis = []
explosoes = []

pause = False

rodando = True

while rodando:

    clock.tick(60)

    for evento in pg.event.get():

        if evento.type == pg.QUIT:
            rodando = False

        if evento.type == pg.KEYDOWN:

            if evento.key == pg.K_ESCAPE:
                pause = not pause

            if pause and evento.key == pg.K_m:

                pg.quit()

                subprocess.run([sys.executable,os.path.join( "Menu.py")])

                sys.exit()

        if not pause:

            if evento.type == pg.MOUSEBUTTONDOWN:

                mx, my = pg.mouse.get_pos()

                som_tiro.play()

                projeteis.append(
                    Projetil(
                        jogador.x,
                        jogador.y,
                        mx,
                        my,
                        jogador.stats["VELOCIDADE_TIRO"]
                    )
                )

    tela.fill(vg.PRETO)

    if not pause:

        teclas = pg.key.get_pressed()

        jogador.mover(teclas)

        for projetil in projeteis[:]:


            projetil.mover()

            distancia = math.sqrt(
                (projetil.x - inimigo.x) ** 2 +
                (projetil.y - inimigo.y) ** 2
            )

            if distancia < projetil.raio + inimigo.raio:

                utils.TomarDano(inimigo, jogador)

                explosoes.append(
                    Explosao(
                        projetil.x,
                        projetil.y
                    )
                )

                projeteis.remove(projetil)

            elif projetil.fora_da_tela():

                projeteis.remove(projetil)

        for explosao in explosoes[:]:

            explosao.atualizar()

            if explosao.tempo <= 0:

                explosoes.remove(explosao)

        if inimigo.stats["VIDA_ATUAL"] <= 0:

            inimigo = Inimigo()

    jogador.desenhar()

    inimigo.desenhar()

    for projetil in projeteis:

        projetil.desenhar()

    for explosao in explosoes:

        explosao.desenhar()

    texto = fonte.render(
        f"Vida do inimigo: {inimigo.stats["VIDA_ATUAL"]}",
        True,
        vg.BRANCO
    )

    tela.blit(texto, (20, 20))

    if pause:

        texto_menu = fonte.render(
            "Pressione M para voltar ao menu",
            True,
            vg.BRANCO
        )

        tela.blit(
            texto_menu,
            (
                vg.LARGURA // 2 - texto_menu.get_width() // 2,
                vg.ALTURA // 2 + 50
            )
        )

        overlay = pg.Surface(
            (vg.LARGURA, vg.ALTURA)
        )

        overlay.set_alpha(180)

        overlay.fill(vg.CINZA)

        tela.blit(overlay, (0, 0))

        texto_pause = fonte_pause.render(
            "PAUSADO",
            True,
            vg.BRANCO
        )

        tela.blit(
            texto_pause,
            (
                vg.LARGURA // 2 - texto_pause.get_width() // 2,
                vg.ALTURA // 2 - 30
            )
        )

    pg.display.update()

pg.quit()