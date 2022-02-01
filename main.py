import pygame
import sys

class Ball( object ):
	def __init__(self, x, y, radius, color):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color


if __name__ == '__main__':
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Projectile')
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)
