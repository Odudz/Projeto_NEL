import pygame as pg

# pygame inicialização
pg.init()

import os, subprocess, sys
import gif_pygame as gifpg
from Modulos import Variaveis_Globais as vg
from Modulos import utils

tela = pg.display.set_mode((vg.LARGURA, vg.ALTURA))
clock = pg.time.Clock()
running = True

# IMAGENS:
fundo_original = pg.image.load(os.path.join( "Imagens", "Menu", "fundoFaroeste.jpeg")).convert()
fundo = pg.transform.scale(fundo_original, tela.get_size())

titulo_nome_original = pg.image.load(os.path.join( "Imagens", "Menu", "titulo_nome.png"))
titulo_nome = pg.transform.scale(titulo_nome_original, (1280 // 2, 720 // 2))

# GIF
backgroundGif = gifpg.load(os.path.join("Imagens", "Menu", "Arbusto_Rolante.gif"))
gif_x = -200
gif_y = 400

#Musica de fundo
MUSICA_FUNDO = pg.mixer_music.load(os.path.join( vg.SONS, "musica_fundo.mp3"))
pg.mixer.music.play(-1)

def creditos():
    vg.tela.fill(vg.PRETO)

    textos = [
        "'ESC' para sair",
        "Programacao: ",
        "Eduardo Pimenta, "
        "Natália Sales, "
        "Leonardo Portes, "
        "",
        "Arte:",
        "@Ghilphea, @gui.h2006",
        "",
        "Musicas:",
        "",
        "Efeitos especiais",
        "Juliano Jeremias, "
        "Pedro Viana"
    ]

    y = 50

    for texto in textos:
        render = vg.fonte_creditos.render(texto, True, vg.BRANCO)
        rect = render.get_rect(center=(640, y))
        vg.tela.blit(render, rect)
        y += 50


#Para funcionamento dos creditos
tela_atual = "menu"

# =========================
# FUNÇÃO DO BOTÃO
# =========================
ultimo_clique = 0


# LOOP PRINCIPAL
while running:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                tela_atual = "menu"

    if tela_atual == "menu":

        tela.blit(fundo, (0, 0))

        backgroundGif.render(tela, (gif_x, gif_y))

        tela.blit(titulo_nome, (325, 50))

        if utils.criar_botao_imagem("Começar jogo", vg.botao_folder, 640, 400):
            pg.quit()
            subprocess.run(
                [sys.executable, "-m", "Modulos.Jogo"],
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            sys.exit()

        if utils.criar_botao_imagem("Créditos", vg.botao_folder, 640, 500):
            tela_atual = "creditos"

        if utils.criar_botao_imagem("Sair", vg.botao_folder, 640, 600):
            running = False

    elif tela_atual == "creditos":
        creditos()

    pg.display.flip()
    clock.tick(60)

pg.quit()