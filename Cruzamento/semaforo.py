import threading
import pygame
import time

class Semaforo(threading.Thread):
	def __init__(self, x, y, surface, sentido, threadId=-1):
		threading.Thread.__init__(self)
		self.imgSemaforoHorizontal_Verde = pygame.image.load("img\SemaforoHorizontal\semaforoHorizontal_Verde.png")
		self.imgSemaforoHorizontal_Amarelo = pygame.image.load("img\SemaforoHorizontal\semaforoHorizontal_Amarelo.png")
		self.imgSemaforoHorizontal_Vermelho = pygame.image.load("img\SemaforoHorizontal\semaforoHorizontal_Vermelho.png")
		self.imgSemaforoVertical_Verde = pygame.image.load("img\SemaforoVertical\semaforoVertical_Verde.png")
		self.imgSemaforoVertical_Amarelo = pygame.image.load("img\SemaforoVertical\semaforoVertical_Amarelo.png")
		self.imgSemaforoVertical_Vermelho = pygame.image.load("img\SemaforoVertical\semaforoVertical_Vermelho.png")

		self.x = x
		self.y = y
		self.surface = surface
		self.sentido = sentido
		self.threadId = threadId
		self.estadoAnterior = "aberto"
		self.estado = "fechado"
		self.cor = "vermelho"
		self.running = False

		if self.sentido == "horizontal":
			surface.blit(self.imgSemaforoHorizontal_Vermelho, [self.x, self.y])
		elif self.sentido == "vertical":
			surface.blit(self.imgSemaforoVertical_Vermelho, [self.x, self.y])

	def setCorSinal(self, cor):
		lock = threading.Lock()
		lock.acquire()
		self.cor = cor
		if self.sentido == "horizontal":
			if cor == "verde":
				self.surface.blit(self.imgSemaforoHorizontal_Verde, [self.x, self.y])
			if cor == "amarelo":
				self.surface.blit(self.imgSemaforoHorizontal_Amarelo, [self.x, self.y])
			if cor == "vermelho":
				self.surface.blit(self.imgSemaforoHorizontal_Vermelho, [self.x, self.y])

		elif self.sentido == "vertical":
			if cor == "verde":
				self.surface.blit(self.imgSemaforoVertical_Verde, [self.x, self.y])
			if cor == "amarelo":
				self.surface.blit(self.imgSemaforoVertical_Amarelo, [self.x, self.y])
			if cor == "vermelho":
				self.surface.blit(self.imgSemaforoVertical_Vermelho, [self.x, self.y])

		lock.release()

	def mudaSinal(self, tempo=2):
		if self.estado == "aberto":
			# self.estado = "aberto"
			self.setCorSinal("verde")
			time.sleep(tempo)
			self.setCorSinal("amarelo")
			time.sleep(tempo)
			self.setCorSinal("vermelho")
			time.sleep(tempo)

		if self.estado == "fechado":
			# self.estado = "fechado"
			self.setCorSinal("verde")
			time.sleep(tempo)
			self.setCorSinal("amarelo")
			time.sleep(tempo)
			self.setCorSinal("vermelho")
			time.sleep(tempo)

	def setEstadoSinal(self, estado="fechado"):
		self.estadoAnterior = self.estado
		self.estado = estado

	def stop(self):
		self.running = False

	def run(self):
		self.running = True
		while self.running:
			if(self.estadoAnterior != self.estado):
				self.mudaSinal()
				print("mudou")
				time.sleep(0.001)

			print(self.estadoAnterior + "  |  " + self.estado)

	def draw(self):
			self.setCorSinal(self.cor)


