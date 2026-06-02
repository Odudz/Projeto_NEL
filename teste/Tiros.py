import pygame as pg, os, random, math, subprocess,sys

pg.init()

#Som tiro
som_tiro = pg.mixer.Sound(os.path.join("Tiros", "Sons", "tiro_som.ogg"))

LARGURA = 1280
ALTURA = 720

tela = pg.display.set_mode((LARGURA, ALTURA))
pg.display.set_caption("Sistema de Tiros")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 100, 255)
AMARELO = (255, 255, 0)
CINZA = (40, 40, 40)

clock = pg.time.Clock()

fonte = pg.font.SysFont("Arial", 28)
fonte_pause = pg.font.SysFont("Arial", 60)


class Jogador:
    def __init__(self):
        self.x = 100
        self.y = ALTURA // 2
        self.vel = 5
        self.raio = 25
        self.vida = 150

    def mover(self, teclas):
        if teclas[pg.K_w]:
            self.y -= self.vel

        if teclas[pg.K_s]:
            self.y += self.vel

        if teclas[pg.K_a]:
            self.x -= self.vel

        if teclas[pg.K_d]:
            self.x += self.vel

        self.x = max(self.raio, min(LARGURA - self.raio, self.x))
        self.y = max(self.raio, min(ALTURA - self.raio, self.y))

    def desenhar(self):
        pg.draw.circle(
            tela,
            AZUL,
            (self.x, self.y),
            self.raio
        )

        pg.draw.rect(
            tela,
            VERMELHO,
            (self.x - 45, self.y - 45, 90, 8)
        )

        pg.draw.rect(
            tela,
            AMARELO,
            (
            self.x - 45,
            self.y - 45,
            60 * (self.vida / 100),
            8
        )
    )


class Inimigo:
    def __init__(self):
        self.x = random.randint(500, 850)
        self.y = random.randint(50, 550)
        self.raio = 30
        self.vida = 100
        self.danoi = 5
        self.vel = 2
        self.tempo_tiro = 0
        self.intervalo_tiro = 120

    def mover(self, jogador):
        dx = jogador.x - self.x
        dy = jogador.y - self.y

        distancia = math.sqrt(dx ** 2 + dy ** 2)

        distancia_minima = jogador.raio + self.raio + 2

        if distancia > distancia_minima:
            self.x += (dx / distancia) * self.vel
            self.y += (dy / distancia) * self.vel

    def desenhar(self):
        pg.draw.circle(
            tela,
            VERMELHO,
            (self.x, self.y),
            self.raio
        )

        pg.draw.rect(
            tela,
            VERMELHO,
            (self.x - 30, self.y - 45, 60, 8)
        )

        pg.draw.rect(
            tela,
            VERDE,
            (
                self.x - 30,
                self.y - 45,
                60 * (self.vida / 100),
                8
            )
        )


class Projetil:
    def __init__(self, x, y, alvo_x, alvo_y):
        self.x = x
        self.y = y
        self.raio = 6
        self.vel = 10

        dx = alvo_x - x
        dy = alvo_y - y

        distancia = math.sqrt(dx**2 + dy**2)

        self.dx = dx / distancia
        self.dy = dy / distancia

        self.dano = random.randint(10, 25)

    def mover(self):
        self.x += self.dx * self.vel
        self.y += self.dy * self.vel

    def desenhar(self):
        pg.draw.circle(
            tela,
            AMARELO,
            (int(self.x), int(self.y)),
            self.raio
        )

    def fora_da_tela(self):
        return (
            self.x < 0 or
            self.x > LARGURA or
            self.y < 0 or
            self.y > ALTURA
        )

class Projetil_inimigo:
    def __init__(self, x, y, alvo_x, alvo_y):
        self.x = x
        self.y = y
        self.raio = 8
        self.vel = 7
        self.dano = 10

        dx = alvo_x - x
        dy = alvo_y - y

        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if distancia == 0:
            distancia = 1

        self.dx = dx / distancia
        self.dy = dy / distancia

    def mover(self):
        self.x += self.dx * self.vel
        self.y += self.dy * self.vel

    def desenhar(self):
        pg.draw.circle(
            tela,
            VERMELHO,
            (int(self.x), int(self.y)),
            self.raio
        )

    def fora_da_tela(self):
        return(
            self.x < 0 or
            self.x > LARGURA or
            self.y < 0 or
            self.y > ALTURA
        )

class Explosao:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.raio = 5
        self.tempo = 20

    def atualizar(self):
        self.raio += 2
        self.tempo -= 1

    def desenhar(self):
        pg.draw.circle(
            tela,
            (255, 150, 0),
            (int(self.x), int(self.y)),
            self.raio,
            3
        )

def criar_wave(quantidade):
    lista = []

    for i in range(quantidade):
        lista.append(Inimigo())

    return lista

jogador = Jogador()

tempo_dano = 0

projeteis = []
explosoes = []
projeteis_inimigo = []
inimigos = []

wave = 1
quantidade_inimigos = 5

inimigos = criar_wave(quantidade_inimigos)

pause = False
gamer_over = False

rodando = True

while rodando:

    clock.tick(60)

    if not gamer_over:
        tempo_dano += 1

    for evento in pg.event.get():

        if evento.type == pg.QUIT:
            rodando = False

        if evento.type == pg.KEYDOWN:

            if evento.key == pg.K_ESCAPE and not gamer_over:
                pause = not pause

            if evento.key == pg.K_r and gamer_over:
                jogador = Jogador()
                wave = 1
                quantidade_inimigos = 5
                inimigos = criar_wave(quantidade_inimigos)

                projeteis.clear()
                explosoes.clear()
                projeteis_inimigo.clear()

                tempo_dano = 0

                gamer_over = False
                pause = False

            if evento.key == pg.K_m and (pause or gamer_over):
                pg.quit()

                subprocess.run([
                    sys.executable,
                    os.path.join("..", "Menu", "Menu.py")
                ])

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
                        my
                    )
                )

    tela.fill(PRETO)

    if not pause and not gamer_over:

        teclas = pg.key.get_pressed()

        x_antigo = jogador.x
        y_antigo = jogador.y

        jogador.mover(teclas)

        for inimigo in inimigos:
            inimigo.mover(jogador)

            inimigo.tempo_tiro += 1

            if inimigo.tempo_tiro >= inimigo.intervalo_tiro:
                som_tiro.play()
                projeteis_inimigo.append( Projetil_inimigo(
                    inimigo.x,
                    inimigo.y,
                    jogador.x,
                    jogador.y
                ))

                inimigo.tempo_tiro = 0

        for inimigo in inimigos:

            distancia_player = math.sqrt(
                (jogador.x - inimigo.x) ** 2 +
                (jogador.y - inimigo.y) ** 2
            )

            if distancia_player < jogador.raio + inimigo.raio:

                jogador.x = x_antigo
                jogador.y = y_antigo

                if tempo_dano >= 15 and jogador.vida > 0:

                    jogador.vida -= inimigo.danoi

                    if jogador.vida < 0:
                        jogador.vida = 0

                    tempo_dano = 0

        for projetil in projeteis[:]:

            projetil.mover()

            for inimigo in inimigos[:]:

                distancia = math.sqrt(
                    (projetil.x - inimigo.x) ** 2 +
                    (projetil.y - inimigo.y) ** 2
                )

                if distancia < projetil.raio + inimigo.raio:

                    inimigo.vida -= projetil.dano

                    explosoes.append(
                        Explosao(
                            projetil.x,
                            projetil.y
                        )
                    )

                    if projetil in projeteis:
                        projeteis.remove(projetil)

                    if inimigo.vida <= 0:
                        inimigos.remove(inimigo)
                    break

        if len(inimigos) == 0:
            wave += 1

            quantidade_inimigos += 2

            inimigos = criar_wave(quantidade_inimigos)

        for projetil in projeteis_inimigo[:]:

            projetil.mover()

            distancia = math.sqrt(
                (projetil.x - jogador.x) ** 2 + (projetil.y - jogador.y) ** 2
            )

            if distancia < projetil.raio + jogador.raio:
                jogador.vida -= projetil.dano

                if jogador.vida < 0:
                    jogador.vida = 0
                    gamer_over = True

                explosoes.append(
                    Explosao(
                        projetil.x,
                        projetil.y
                    )
                )

                projeteis_inimigo.remove(projetil)

            elif projetil.fora_da_tela():
                projeteis_inimigo.remove(projetil)


        for explosao in explosoes[:]:

            explosao.atualizar()

            if explosao.tempo <= 0:

                explosoes.remove(explosao)

        if jogador.vida == 0:

            gamer_over = True

    jogador.desenhar()

    for inimigo in inimigos:
        inimigo.desenhar()

    for projetil in projeteis:

        projetil.desenhar()

    for projetil in projeteis_inimigo:
        projetil.desenhar()

    for explosao in explosoes:

        explosao.desenhar()

    texto = fonte.render(
        f"Qunatidade de inimigos: {len(inimigos)}",
        True,
        BRANCO
    )

    tela.blit(texto, (20, 20))

    texto = fonte.render(
        f"Vida do Player: {jogador.vida}",
        True,
        BRANCO
    )

    tela.blit(texto, (20, 60))

    texto = fonte.render(
        f"Wave: {wave}",
        True,
        BRANCO
    )

    tela.blit(texto, (20, 120))

    if pause:

        texto_menu = fonte.render(
            "Pressione M para voltar ao menu",
            True,
            BRANCO
        )

        tela.blit(
            texto_menu,
            (
                LARGURA // 2 - texto_menu.get_width() // 2,
                ALTURA // 2 + 50
            )
        )

        overlay = pg.Surface(
            (LARGURA, ALTURA)
        )

        overlay.set_alpha(180)

        overlay.fill(CINZA)

        tela.blit(overlay, (0, 0))

        texto_pause = fonte_pause.render(
            "PAUSADO",
            True,
            BRANCO
        )

        tela.blit(
            texto_pause,
            (
                LARGURA // 2 - texto_pause.get_width() // 2,
                ALTURA // 2 - 30
            )
        )

    if gamer_over:

        overlay = pg.Surface((LARGURA, ALTURA))
        overlay.set_alpha(200)
        overlay.fill(CINZA)

        tela.blit(overlay, (0, 0))

        texto_morte = fonte_pause.render(
            "Você Morreu!",
            True,
            VERMELHO
        )

        tela.blit(
            texto_morte,
            (LARGURA // 2 - texto_morte.get_width() // 2,
             ALTURA // 2 - 80)
        )

        texto_recomecar = fonte.render(
            "Pressione R para reiniciar",
            True,
            BRANCO
        )

        tela.blit(
            texto_recomecar,
            (LARGURA // 2 - texto_recomecar.get_width() // 2,
             ALTURA // 2 + 10)
        )

        texto_menu = fonte.render(
            "Pressione M para voltar ao menu",
            True,
            BRANCO
        )

        tela.blit(
            texto_menu,
            (LARGURA // 2 - texto_menu.get_width() // 2,
             ALTURA // 2 + 50)
        )

    pg.display.update()

pg.quit()