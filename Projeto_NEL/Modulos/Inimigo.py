import pygame as pg

class Inimigo:
    def __init__(self):
        self.x = random.randint(500, 850)
        self.y = random.randint(50, 550)
        self.raio = 30

        self.stats = StatusInimigo()

    def mover(self, jogador):
        dx = jogador.x - self.x
        dy = jogador.y - self.y

        distancia = math.sqrt(dx ** 2 + dy ** 2)

        distancia_minima = jogador.raio + self.raio + 2

        if distancia > distancia_minima:
            self.x += (dx / distancia) * self.stats["VELOCIDADE"]
            self.y += (dy / distancia) * self.stats["VELOCIDADE"]

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
            (self.x - 30, self.y - 45, 60, 8)
        )

        pg.draw.rect(
            vg.tela,
            vg.VERDE,
            (
                self.x - 30,
                self.y - 45,
                60 * (self.stats["VIDA_ATUAL"] / self.stats["VIDA_MAXIMA"]),
                8
            )
        )
