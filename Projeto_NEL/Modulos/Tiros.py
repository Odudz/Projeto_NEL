import pygame as pg
import Variaveis_Globais as vg
import random, math, subprocess, sys, os

pg.init()

#Som tiro
som_tiro = pg.mixer.Sound(os.path.join("Projeto_NEL", vg.SONS, "tiro_som.ogg"))

tela = pg.display.set_mode((vg.LARGURA, vg.ALTURA))
pg.display.set_caption("Sistema de Tiros")

clock = pg.time.Clock()

fonte = pg.font.SysFont("Arial", 28)
fonte_pause = pg.font.SysFont("Arial", 60)


class Jogador:
    def __init__(self):
        self.x = 100
        self.y = vg.ALTURA // 2
        self.vel = 5
        self.raio = 25

    def mover(self, teclas):
        if teclas[pg.K_w]:
            self.y -= self.vel

        if teclas[pg.K_s]:
            self.y += self.vel

        if teclas[pg.K_a]:
            self.x -= self.vel

        if teclas[pg.K_d]:
            self.x += self.vel

        self.x = max(self.raio, min(vg.LARGURA - self.raio, self.x))
        self.y = max(self.raio, min(vg.ALTURA - self.raio, self.y))

    def desenhar(self):
        pg.draw.circle(
            tela,
            vg.AZUL,
            (self.x, self.y),
            self.raio
        )


class Inimigo:
    def __init__(self):
        self.x = random.randint(500, 850)
        self.y = random.randint(50, 550)
        self.raio = 30
        self.vida = 100

    def desenhar(self):
        pg.draw.circle(
            tela,
            vg.VERMELHO,
            (self.x, self.y),
            self.raio
        )

        pg.draw.rect(
            tela,
            vg.VERMELHO,
            (self.x - 30, self.y - 45, 60, 8)
        )

        pg.draw.rect(
            tela,
            vg.VERDE,
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
            vg.AMARELO,
            (int(self.x), int(self.y)),
            self.raio
        )

    def fora_da_tela(self):
        return (
            self.x < 0 or
            self.x > vg.LARGURA or
            self.y < 0 or
            self.y > vg.ALTURA
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


jogador = Jogador()
inimigo = Inimigo()

projeteis = []
explosoes = []

pause = False

rodando = True

while rodando:

    clock.tick(60)

    for evento in pg.event.get():

        if evento.type == pg.QUIT:
            rodando = False

        if evento.type == pg.KEYDOWN:

            if evento.key == pg.K_ESCAPE:
                pause = not pause

            if pause and evento.key == pg.K_m:

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

    tela.fill(vg.PRETO)

    if not pause:

        teclas = pg.key.get_pressed()

        jogador.mover(teclas)

        for projetil in projeteis[:]:


            projetil.mover()

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

                projeteis.remove(projetil)

            elif projetil.fora_da_tela():

                projeteis.remove(projetil)

        for explosao in explosoes[:]:

            explosao.atualizar()

            if explosao.tempo <= 0:

                explosoes.remove(explosao)

        if inimigo.vida <= 0:

            inimigo = Inimigo()

    jogador.desenhar()

    inimigo.desenhar()

    for projetil in projeteis:

        projetil.desenhar()

    for explosao in explosoes:

        explosao.desenhar()

    texto = fonte.render(
        f"Vida do inimigo: {inimigo.vida}",
        True,
        vg.BRANCO
    )

    tela.blit(texto, (20, 20))

    if pause:

        texto_menu = fonte.render(
            "Pressione M para voltar ao menu",
            True,
            vg.BRANCO
        )

        tela.blit(
            texto_menu,
            (
                vg.LARGURA // 2 - texto_menu.get_width() // 2,
                vg.ALTURA // 2 + 50
            )
        )

        overlay = pg.Surface(
            (vg.LARGURA, vg.ALTURA)
        )

        overlay.set_alpha(180)

        overlay.fill(vg.CINZA)

        tela.blit(overlay, (0, 0))

        texto_pause = fonte_pause.render(
            "PAUSADO",
            True,
            vg.BRANCO
        )

        tela.blit(
            texto_pause,
            (
                vg.LARGURA // 2 - texto_pause.get_width() // 2,
                vg.ALTURA // 2 - 30
            )
        )

    pg.display.update()

pg.quit()