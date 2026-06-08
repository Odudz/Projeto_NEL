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

