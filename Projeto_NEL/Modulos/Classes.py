import pygame as pg
import os

# pygame inicialização
pg.init()

import Variaveis_Globais as vg
import random, math
from utils import StatusInimigo

class Jogador:
    def __init__(self):
        #Status base do player

        tamanho_sprite = (80, 80)

        self.sprite_w = pg.transform.scale(
            pg.image.load(os.path.join("Imagens", "Jogo", "atirando_w.png")).convert_alpha(),
            tamanho_sprite
        )

        self.sprite_s = pg.transform.scale(
            pg.image.load(os.path.join("Imagens", "Jogo", "atirando_s.png")).convert_alpha(),
            tamanho_sprite
        )

        self.sprite_a = pg.transform.scale(
            pg.image.load(os.path.join("Imagens", "Jogo", "atirando_a.png")).convert_alpha(),
            tamanho_sprite
        )

        self.sprite_d = pg.transform.scale(
            pg.image.load(os.path.join("Imagens", "Jogo", "aitando_d.png")).convert_alpha(),
            tamanho_sprite
        )

        self.sprite = self.sprite_s

        self.stats = {
            "VIDA_ATUAL"      : 100, # Vida Atual
            "VIDA_MAXIMA"     : 100, # Vida máxima
            "DANO"            : 10,  # Dano base
            "VELOCIDADE"      : 5,   # Velocidade do player
            "TAXA_ATAQUES"    : 500, # Tempo em milissegundos entre os tiros
            "VELOCIDADE_TIRO" : 10,  # Velocidade do tiro
            "QUANTIDADE_TIRO" : 1,   # Quantidade de tiros disparados de uma vez
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
            self.sprite = self.sprite_w

        if teclas[pg.K_s]:
            y += self.vel
            self.sprite = self.sprite_s

        if teclas[pg.K_a]:
            x -= self.vel
            self.sprite = self.sprite_a

        if teclas[pg.K_d]:
            x += self.vel
            self.sprite = self.sprite_d

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
        vg.tela.blit(
            self.sprite,
            (
                self.x - self.sprite.get_width() // 2,
                self.y - self.sprite.get_height() // 2
            )
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

class ProjetilInimigo:
    def __init__(self, x, y, alvo_x, alvo_y, stats):
        self.x = x
        self.y = y
        self.raio = 8
        self.vel = stats["VELOCIDADE_TIRO"]
        self.dano = stats["DANO"]

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
            vg.tela,
            vg.VERMELHO,
            (int(self.x), int(self.y)),
            self.raio
        )

    def fora_da_tela(self):
        return(
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