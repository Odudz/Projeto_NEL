import os, subprocess, sys
import gif_pygame as gifpg
from Modulos import Variaveis_Globais as vg

try:
    import pygame as pg
except ImportError:
    print("Erro no import.")
    sys.exit(2)

# pygame inicialização
pg.init()

tela = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

# FONTES
fonte = pg.font.SysFont("arial", 35)
fonte_nome_menu = pg.font.SysFont("arial", 70)
fonte_creditos = pg.font.SysFont("arial", 25)

# IMAGENS:
fundo_original = pg.image.load(os.path.join( "Imagens", "Menu", "fundoFaroeste.jpeg")).convert()
fundo = pg.transform.scale(fundo_original, tela.get_size())

titulo_nome_original = pg.image.load(os.path.join( "Imagens", "Menu", "titulo_nome.png"))
titulo_nome = pg.transform.scale(titulo_nome_original, (1280 // 2, 720 // 2))

botao_folder_original = pg.image.load(os.path.join( "Imagens", "Menu", "botao_folder.png"))
botao_folder = pg.transform.scale(botao_folder_original, (400,200))

# GIF
backgroundGif = gifpg.load(os.path.join("Imagens", "Menu", "Arbusto_Rolante.gif"))
gif_x = -200
gif_y = 400


#Musica de fundo
MUSICA_FUNDO = pg.mixer_music.load(os.path.join( vg.SONS, "musica_fundo.mp3"))
pg.mixer.music.play(-1)


#Para funcionamento dos creditos
tela_atual = "menu"

# =========================
# FUNÇÃO DO BOTÃO
# =========================
ultimo_clique = 0

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
    tela.blit(imagem, botao)


    # 2. Renderiza e centraliza o texto por cima da imagem
    texto_render = fonte.render(texto, True, vg.BRANCO)
    texto_rect = texto_render.get_rect(center=botao.center)
    tela.blit(texto_render, texto_rect)

    return clicou

def creditos():
    tela.fill(vg.PRETO)

    textos = [
        "Projeto NEL",
        "",
        "Programacao:",
        "Eduardo Pimenta",
        "Natália Sales",
        "Leonardo Portes",
        "",
        "Arte:",
        "@Ghilphea",
        "",
        "Musicas:",
        "Ciclano",
        "Juliano Jeremias",
        "",
        "ESC para voltar"
    ]

    y = 50

    for texto in textos:
        render = fonte_creditos.render(texto, True, vg.BRANCO)
        rect = render.get_rect(center=(640, y))
        tela.blit(render, rect)
        y += 50

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

        if criar_botao_imagem("Começar jogo", botao_folder, 640, 400):
            pg.quit()
            subprocess.run([sys.executable, os.path.join("Modulos", "Tiros.py")])
            sys.exit()

        if criar_botao_imagem("Créditos", botao_folder, 640, 500):
            tela_atual = "creditos"

        if criar_botao_imagem("Sair", botao_folder, 640, 600):
            running = False

    elif tela_atual == "creditos":
        creditos()

    pg.display.flip()
    clock.tick(60)

pg.quit()
