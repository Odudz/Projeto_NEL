import pygame as pg
import Variaveis_Globais as vg
import random, math, sys, os
from utils import StatusInimigo

class Jogador:
    def __init__(self):
        #Status base do player
        self.stats = {
            "VIDA_ATUAL"      : 100, # Vida Atual
            "VIDA_MAXIMA"     : 100, # Vida máxima
            "DANO"            : 10,  # Dano base
            "VELOCIDADE"      : 5,   # Velocidade do player
            "TAXA_ATAQUES"    : 500, # Tempo em milissegundos entre os tiros
            "VELOCIDADE_TIRO" : 10,  # Velocidade do tiro
            "QUANTIDADE_TIRO" : 3,   # Quantidade de tiros disparados de uma vez
            "CHANCE_CRITICO"  : 25,  # Chance de critico %
            "DANO_CRITICO"    : 2,   # Quantia que multiplicará em caso de critico
        }

        #Posição do player
        self.x = 100
        self.y = vg.ALTURA // 2

        self.raio = 25
        self.vel = self.stats["VELOCIDADE"]

        #Sprites utilizados
        self.anim = [
            #pg.image.load(os.path.join('IMAGES', 'Sheriff', "Jogador_Parado.png")).convert_alpha(),
            #pg.image.load(os.path.join('IMAGES', "Jogador_ParadoDireita.png")).convert_alpha(),
            #pg.image.load(os.path.join('IMAGES', "Jogador_ParadoEsquerda.png")).convert_alpha(),
            #pg.image.load(os.path.join('IMAGES', 'Sheriff', "Jogador_ParadoCostas.png")).convert_alpha(),
        ]

    def mover(self, teclas):
        y = 0
        x = 0

        #Define velocidade na direção baseado na tecla apertada
        if teclas[pg.K_w]:
            y -= self.vel

        if teclas[pg.K_s]:
            y += self.vel

        if teclas[pg.K_a]:
            x -= self.vel

        if teclas[pg.K_d]:
            x += self.vel

        #Reduz a velocidade em diagonais
        if x != 0 and y != 0:
            x /= 1.5
            y /= 1.5

        #Aplica a distância andada
        self.x += x
        self.y += y

        #Limita as bordas da tela
        self.x = max(self.raio, min(vg.LARGURA - self.raio, self.x))
        self.y = max(self.raio, min(vg.ALTURA - self.raio, self.y))


    def desenhar(self):
        pg.draw.circle(
            vg.tela,
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

        self.stats = StatusInimigo()

    def desenhar(self):
        pg.draw.circle(
            vg.tela,
            vg.VERMELHO,
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


class Projetil:
    def __init__(self, x, y, alvo_x, alvo_y, vel):
        self.x = x
        self.y = y
        self.raio = 6
        self.vel = vel

        dx = alvo_x - x
        dy = alvo_y - y

        distancia = math.sqrt(dx**2 + dy**2)

        self.dx = dx / distancia
        self.dy = dy / distancia

    def mover(self):
        self.x += self.dx * self.vel
        self.y += self.dy * self.vel

    def desenhar(self):
        pg.draw.circle(
            vg.tela,
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
            vg.tela,
            (255, 150, 0),
            (int(self.x), int(self.y)),
            self.raio,
            3
        )