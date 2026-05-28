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
fundo_original = pg.image.load(os.path.join("imgTeste", "fundoFaroeste.jpeg")).convert()
fundo = pg.transform.scale(fundo_original, tela.get_size())

titulo_nome_original = pg.image.load(os.path.join("imgTeste", "titulo_nome.png"))
titulo_nome = pg.transform.scale(titulo_nome_original, (1280 // 2, 720 // 2))

botao_folder_original = pg.image.load(os.path.join("imgTeste", "botao_folder.png"))
botao_folder = pg.transform.scale(botao_folder_original, (230,70))

# GIF
backgroundGif = gifpg.load(os.path.join("imgTeste", "Arbusto_Rolante.gif"))
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

def criar_botao_imagem(texto, imagem, x, y):
    global ultimo_clique

    mouse = pg.mouse.get_pos()
    clique = pg.mouse.get_pressed()

    # Cria o retângulo com base na posição (x, y) e tamanho da imagem
    botao = imagem.get_rect(topleft=(x, y))

    agora = pg.time.get_ticks()
    clicou = False

    if botao.collidepoint(mouse):
        # Verifica clique + cooldown
        if clique[0] and agora - ultimo_clique > 2000:
            ultimo_clique = agora
            clicou = True

    # 1. Desenha a imagem do botão na tela
    tela.blit(imagem, botao)

    # 2. Renderiza e centraliza o texto por cima da imagem
    texto_render = fonte.render(texto, True, branco)
    texto_rect = texto_render.get_rect(center=botao.center)
    tela.blit(texto_render, texto_rect)

    return clicou



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
    tela.blit(titulo_nome, (340,50))

    # BOTÃO jogar
    if criar_botao_imagem("Começar jogo",botao_folder , 540, 400):
        print("Jogo iniciado!")
    if criar_botao_imagem("Sair",botao_folder,540, 600):
        pg.quit()

    pg.display.flip()
    clock.tick(60)

pg.quit()