import os.path
import sys
import gif_pygame as gifpg

try:
    import pygame as pg
except ImportError:
    print("couldn't load module.")
    sys.exit(2)

# pygame inicialização
pg.init()

tela = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

# FONTES
fonte = pg.font.SysFont("arial", 35)
fonte_nome_menu = pg.font.SysFont("arial", 70)

# IMAGENS:
fundo_original = pg.image.load(
    os.path.join("imgTeste", "fundoFaroeste.jpeg")
).convert()

fundo = pg.transform.scale(fundo_original, tela.get_size())

# GIF
backgroundGif = gifpg.load(
    os.path.join("imgTeste", "Arbusto_Rolante.gif")
)

gif_x = -200
gif_y = 400

# CORES
vermelho = (255, 0, 0)
marrom = (150,75,0)
marrom_claro = (180,100,29)
branco = (255, 255, 255)


# =========================
# FUNÇÃO DO BOTÃO
# =========================
ultimo_clique = 0

def criar_botao(texto, x, y, largura, altura):

    global ultimo_clique

    mouse = pg.mouse.get_pos()
    clique = pg.mouse.get_pressed()

    botao = pg.Rect(x, y, largura, altura)

    agora = pg.time.get_ticks()

    if botao.collidepoint(mouse):
        cor = marrom_claro

        # Verifica clique + cooldown
        if clique[0] and agora - ultimo_clique > 2000:

            ultimo_clique = agora
            return True

    else:
        cor = marrom

    pg.draw.rect(tela, cor, botao, border_radius=12)

    texto_render = fonte.render(texto, True, branco)

    texto_rect = texto_render.get_rect(center=botao.center)

    tela.blit(texto_render, texto_rect)

    return False


# LOOP PRINCIPAL
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    #coloca o fundo
    tela.blit(fundo, (0, 0))
    # GIF
    backgroundGif.render(tela, (gif_x, gif_y))

    #Colocar nome do jogo
    texto_nome = fonte_nome_menu.render("Projeto Final - NEL",True,"white", marrom)
    tela.blit(texto_nome, (400, 100))
    #COLOCAR IMAGEM PARA O MENU INICIAL DOQ COLOCAR BOTAO

    # BOTÃO MENU
    if criar_botao("Começar jogo", 540, 300, 230, 70):
        print("Jogo iniciado!")

    pg.display.flip()
    clock.tick(60)

pg.quit()