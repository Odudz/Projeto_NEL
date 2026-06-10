import pygame as pg
import Variaveis_Globais as vg

pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    a


    pg.display.flip()
    clock.tick(60)
pg.quit()