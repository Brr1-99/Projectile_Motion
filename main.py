import pygame
import sys
import math
from settings import *

class Ball( object ):
	def __init__(self, screen, x , y, radius, color):
		self.screen = screen
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
	
	def draw(self):
		pygame.draw.circle(self.screen, self.color, (self.x,self.y) ,self.radius)

	def draw_line(self, mouse_pos):
		pygame.draw.line(self.screen, green, (self.x,self.y), mouse_pos, 2 )
	
	def draw_ball_path (self, pos_list):
		if pos_list:
			for position in pos_list:
				pygame.draw.circle(self.screen, red, position, 2, width=2)
	
	def calculate_angle(self, mouse_pos):
		try :
			angle = math.atan((mouse_pos[1]-self.y)/-(mouse_pos[0]-self.x)) * 180 / math.pi
			angle = 180 + angle if angle < 0 else angle
		except:
			angle = 90
		return angle
	
	@staticmethod
	def next_position(initX, initY, power, angle, time):
		xVelocity = math.cos(angle*math.pi/180)*power
		yVelocity = math.sin(angle*math.pi/180)*power
	
		xDistance = xVelocity * time
		yDistance = (yVelocity * time) + ((-gravity/2*(time**2))/2)

		next_x = round(xDistance + initX)
		next_y = round(initY - yDistance )

		return next_x, next_y

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Projectile Motion')

ball = Ball(screen, initial_pos[0], initial_pos[1], radius , black)

ball_path_list = []
current_mouse_pos = None
clock = pygame.time.Clock()
angle = 0
shoot = False
power = 0
time = 0
bounce = False

def redraw():
	screen.fill(white)
	ball.draw()
	if current_mouse_pos != None:
			ball.draw_line(current_mouse_pos)
	ball.draw_ball_path(ball_path_list)
	pygame.display.update()

if __name__ == '__main__':
	pygame.init()
	while True:
		screen.fill(white)
		clock.tick(fps)

		if shoot:
			if ball.y < height - radius :
				time += 0.03
				next_coordinates = ball.next_position(x, y, power, angle, time)
				ball.x, ball.y = next_coordinates
				if next_coordinates[0] < radius :
					ball.x = radius  + abs(next_coordinates[0]) + 2
					bounce = True
				elif next_coordinates[0] > width - radius:
					ball.x = 2*width - next_coordinates[0] - radius - 1
					bounce = True
				ball_path_list.append((ball.x, ball.y))
			else:
				if power < 1:
					shoot = False
					time = 0
					ball.y = height - radius - 1
					if ball.x < radius or ball.x > width - radius:
						ball.x = initial_pos[0]
				else :
					power /= 1.6
					time = 0.03
					x, y = ball.x, ball.y
					if bounce :
						angle = (180 - angle)
						bounce = False
					next_coordinates = ball.next_position(x, y, power, angle, time)
					ball.x, ball.y = next_coordinates[0], radius


		redraw()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEMOTION:
				current_mouse_pos = event.pos
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if not shoot:
					ball_path_list = []
					x,y = ball.x, ball.y
					mouse_position  = pygame.mouse.get_pos()
					angle = ball.calculate_angle(mouse_position)
					shoot = True
					power = math.sqrt((mouse_position[1]-ball.y)**2 + (mouse_position[0]-ball.x)**2)/8
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					ball.x , ball.y = initial_pos
