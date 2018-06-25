import pygame
from veiculo import Veiculo
from infraestruta import Infraestruta


(width, height) = (1280, 720)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cruzamento')
bg = pygame.image.load("img\Map.png")
screen.blit(bg, [0, 0])
pygame.display.flip()
rect = pygame.Rect(50, 50, 50, 50)
clock = pygame.time.Clock()


def main():
	listaVeiculos = []

	v1 = Veiculo(color=0, threadID=1, limiteVelocidade=140, posicaoInicial=1, posicaoFinal=4)
	v2 = Veiculo(color=50, threadID=2, limiteVelocidade=60, posicaoInicial=2, posicaoFinal=4)
	v3 = Veiculo(color=100, threadID=3, limiteVelocidade=80, posicaoInicial=3, posicaoFinal=1)
	v4 = Veiculo(color=150, threadID=4, limiteVelocidade=100, posicaoInicial=4, posicaoFinal=2)
	v5 = Veiculo(color=200, threadID=5, limiteVelocidade=120, posicaoInicial=4, posicaoFinal=2)
	v6 = Veiculo(color=250, threadID=6, limiteVelocidade=140, posicaoInicial=4, posicaoFinal=2)

	listaVeiculos.append(v1)
	listaVeiculos.append(v2)
	listaVeiculos.append(v3)
	listaVeiculos.append(v4)
	listaVeiculos.append(v5)
	listaVeiculos.append(v6)

	for v in listaVeiculos:
		v.start()

	running = True

	while running:
		screen.blit(bg, [0, 0])
		v1.draw(screen)
		v2.draw(screen)
		v3.draw(screen)
		v4.draw(screen)
		v5.draw(screen)
		v6.draw(screen)

		pygame.display.update()
		clock.tick(30)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				for v in listaVeiculos:
					v.stop()


if __name__ == '__main__':
	pygame.init()
	main()
	pygame.quit()


