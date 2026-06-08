import pygame as pg
import os

LARGURA = 1280
ALTURA = 720

tela = pg.display.set_mode((LARGURA, ALTURA))

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 100, 255)
AMARELO = (255, 255, 0)
CINZA = (40, 40, 40)
ROXO  = (157, 0, 255)

ONDA = 0
INIMIGOS_MORTOS = 0

RAJADA = 0
PROXIMA_RAJADA = 0
RAJADAMX = 0
RAJADAMY = 0

PROXIMO_TIRO = 0

MENU_MELHORIA = False
ESCOLHENDO_MELHORIA = False

UpgradeAleatorio = [
    "Nenhum",
    "Nenhum",
    "Nenhum",
]

IMAGENS = "Imagens"
SONS    = "Sons"

botao_folder_original = pg.image.load(os.path.join( "Imagens", "Menu", "botao_folder.png"))
botao_folder = pg.transform.scale(botao_folder_original, (400,200))

# FONTES
fonte = pg.font.Font("Fonte/texat_bold.otf", 15)
fonte_nome_menu = pg.font.Font("Fonte/texat_bold.otf", 50)
fonte_creditos = pg.font.Font("Fonte/texat_bold.otf", 20)
fonte_jogo = pg.font.Font("Fonte/Western.ttf", 30)