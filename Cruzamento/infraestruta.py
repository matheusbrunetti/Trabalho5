import threading
import time
import pandas as pd
from scipy.spatial import distance_matrix
import pygame

class Infraestruta(threading.Thread):
	listaVeiculos = []
	threadId = -1

	def __init__(self, threadId, listaVeiculos):
		threading.Thread.__init__(self)
		self.threadId = threadId
		self.listaVeiculos = listaVeiculos
		self.running = False
		self.distanciaMinimaEntreVeiculos = 100
		self.regiaoCruzamento = pygame.rect.Rect((562, 284, 153, 153))

	def stop(self):
		self.running = False

	def getPosicoesVeiculos(self):
		posicoes = []
		for v in self.listaVeiculos:
			posicoes.append([v.threadID, v.getPosicao()])
		return posicoes

	def getDistanciaEntreVeiculos(self):
		posicoesVeiculos = self.getPosicoesVeiculos()
		posicoes = []
		veiculos = []

		for i in range(0, len(posicoesVeiculos)):
			veiculos.append(posicoesVeiculos[i][0])
			posicoes.append(posicoesVeiculos[i][1])
		df = pd.DataFrame(posicoes, columns=[0, 1], index=veiculos)

		distancias =  pd.DataFrame(distance_matrix(df.values, df.values), index=df.index, columns=df.index)
		return distancias

	def distanciaMinimaAlcancada(self):
		posicoes = self.getPosicoesVeiculos()
		distancias = self.getDistanciaEntreVeiculos()
		distanciasMinimasAlcancadas = pd.DataFrame(index=range(1, len(self.listaVeiculos)+1), columns=range(1, len(self.listaVeiculos)+1))

		for i in range(1, len(distancias)+1):
			for j in range(1, len(distancias)+1):
				if posicoes[i-1][1] == posicoes[j-1][1]:
					if i == j:
						distanciasMinimasAlcancadas[i][j] = False
						self.listaVeiculos[i - 1].acelera()
					elif distancias[i][j] < 100 and i != j:
						distanciasMinimasAlcancadas[i][j] = True
						#self.listaVeiculos[i-1].freia(distancias[i][j])
						self.listaVeiculos[j-1].acelera()
					else:
						distanciasMinimasAlcancadas[i][j] = False
						self.listaVeiculos[i-1].acelera()

		return distanciasMinimasAlcancadas

	def run(self):
		self.running = True
		while self.running:
			#print(self.getDistanciaEntreVeiculos())
			self.distanciaMinimaAlcancada()
			time.sleep(0.001)

			# for v in self.listaVeiculos:
			# 	v.acelera()
			# 	print(str(v.getVelocidadeRealEmPixels()) + "  " + str(v.getVelocidadeEmKm()))

	def __str__(self):
		return "Infraestrutura Inicializada"




