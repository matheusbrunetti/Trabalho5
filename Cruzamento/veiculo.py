import threading
import time
import pygame
import socket


class Veiculo(threading.Thread):

	def __init__(self, color=255, threadID=-1, W=45, H=45, aceleracao=0.1, limiteVelocidade=100, posicaoInicial = 2, posicaoFinal=3):
		threading.Thread.__init__(self)
		self.aceleracao = aceleracao
		self.H = H
		self.W = W
		self.color = color
		self.threadID = threadID
		self.running = False
		self.velocidade = 0
		self.limiteVelocidade=self.mapArduino(limiteVelocidade,0, 200, 0, 20)
		self.velocidadeEmKm = 0
		self.posicaoInicial = posicaoInicial
		self.posicaoFinal = posicaoFinal
		self.rect = pygame.rect.Rect((-50, -50, W, H))
		if self.posicaoInicial == 1:
			self.rect.x = 0
			self.rect.y = 375
			self.sentido = 1
		elif self.posicaoInicial == 2:
			self.rect.x = 660
			self.rect.y = 700
			self.sentido = -1
		elif self.posicaoInicial == 3:
			self.rect.x = 1280
			self.rect.y = 300
			self.sentido = -1
		elif self.posicaoInicial == 4:
			self.rect.x = 570
			self.rect.y = 0
			self.sentido = 1


		self.host = '127.0.0.1'
		self.port = 5000
		self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.dest = (self.host, self.port)
		self.tcp.connect(self.dest)


	def mapArduino(self, x, in_min, in_max, out_min, out_max):
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

	def freia(self, distancia):
		self.velocidade = self.sentido*round((self.velocidade ** 2 / (2*(distancia + self.sentido*(self.W + self.H)))), 2)

	def getPosicao(self):
		return [self.rect.x, self.rect.y]

	def verificaLimites(self, width = 1280, height = 720):
		if self.rect.x > width + self.W:
			self.rect.x = 0
		elif self.rect.y > height + self.H:
			self.rect.y = 0
		elif self.rect.x < 0  - self.W:
			self.rect.x = width
		elif self.rect.y < 0 - self.H:
			self.rect.y = height

	def draw(self, surface):
		lock = threading.Lock()
		lock.acquire()
		pygame.draw.rect(surface, self.color, self.rect)
		lock.release()

	def acelera(self):
		self.velocidade = round(self.velocidade + self.aceleracao*self.sentido, 2)
		self.setVelocidadeEmKm(self.velocidade)
		return self.velocidade

	def verificaLimiteVelocidade(self):
		if abs(self.getVelocidadeRealEmPixels()) >= self.limiteVelocidade:
			self.setVelocidadeRealEmPixels(self.limiteVelocidade*self.sentido)

		elif abs(self.getVelocidadeRealEmPixels()) < 0:
			self.setVelocidadeRealEmPixels(0)

	def getVelocidadeRealEmPixels(self):
		return self.velocidade

	def setVelocidadeRealEmPixels(self, velocidade):
		self.setVelocidadeEmKm(velocidade)
		self.velocidade = round(velocidade, 2)

	def setVelocidadeEmKm(self, velocidade):
		self.velocidadeEmKm = round(self.mapArduino(self.getVelocidadeRealEmPixels(), 0, 20, 0, 200), 2)

	def getVelocidadeEmKm(self):
		return self.velocidadeEmKm

	def stop(self):
		self.running = False

	def setSentido(self, sentido):
		self.sentido = sentido

	def moveX(self):
		self.rect.move_ip(self.velocidade, 0)

	def moveY(self):
		self.rect.move_ip(0, self.velocidade)

	def verificaCurvas(self):
		if self.posicaoInicial == 1 and self.posicaoFinal == 2:
			if self.rect.x < 575:
				self.moveX()
			else:
				self.moveY()
		elif self.posicaoInicial == 1 and self.posicaoFinal == 3:
			self.moveX()
		elif self.posicaoInicial == 1 and self.posicaoFinal == 4:
			if self.rect.x < 660:
				self.moveX()
			else:
				self.moveY()


		elif self.posicaoInicial == 2 and self.posicaoFinal == 4:
			self.moveY()

		elif self.posicaoInicial == 3 and self.posicaoFinal == 1:
			self.moveX()

		elif self.posicaoInicial == 4 and self.posicaoFinal == 2:
			self.moveY()

	def receiveMsgTCP(self):

		try:
			#print(self.tcp.recv(1024).decode())
			msg = "1/freia/200"
			id, comando, distancia = msg.split("/")
			comando = "acelera"
			id = 1
			distancia = 200
			if id == self.threadID:
				if comando == "acelera":
					self.acelera()
				elif comando == "freia":
					self.freia(distancia)
		except ValueError:
			print("Error")

	def run(self):
		self.running = True
		while self.running:
			self.receiveMsgTCP()
			self.verificaCurvas()
			self.verificaLimites()
			self.verificaLimiteVelocidade()
			self.tcp.send(self.__str__().encode())
			lock = threading.Lock()
			lock.acquire()
			lock.release()
			time.sleep(0.005)

		self.tcp.close()

	def __str__(self):
		return str(self.threadID) + "/" + str(self.getPosicao()[0]) + "/" + str(self.getPosicao()[1])
		#return "Veiculo " + str(self.threadID) + ": " + str(self.getPosicao()) + "\n"







