import pygame as pg
import os

# pygame inicialização
pg.init()

import Variaveis_Globais as vg
import random, math
from utils import StatusChefe

class Chefao:
    def __init__(self):
        self.x = random.randint(500, 850)
        self.y = random.randint(50, 550)
        self.raio = 90

        self.stats = StatusChefe()

    def mover(self, jogador):
        dx = jogador.x - self.x
        dy = jogador.y - self.y

        distancia = math.sqrt(dx ** 2 + dy ** 2)

        distancia_minima = jogador.raio + self.raio + 2

        if distancia > distancia_minima:
            self.x += (dx / distancia) * 0
            self.y += (dy / distancia) * 0

    def desenhar(self):
        pg.draw.circle(
            vg.tela,
            self.stats["COLOR"],
            (self.x, self.y),
            self.raio
        )

        pg.draw.rect(
            vg.tela,
            vg.VERMELHO,
            (
                self.x - self.raio,
                self.y - self.raio * 1.25,
                self.raio * 2,
                13
            )
        )

        pg.draw.rect(
            vg.tela,
            vg.VERDE,
            (
                self.x - self.raio,
                self.y - self.raio * 1.25,
                self.raio * 2 * (self.stats["VIDA_ATUAL"] / self.stats["VIDA_MAXIMA"]),
                13
            )
        )