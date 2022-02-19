import pygame
import math
import random
from objects import Line, Arm



pygame.init()
width=500
height=500
window = pygame.display.set_mode((width, height))
def clear():
	pygame.display.update()
	window.fill((225, 225, 225))
def main():
	running = True
	line = Line(250, 250, angle=0)
	m=False
	bot=Arm(250, 250, 55, 6, 360, joints=True)
	x=random.randint(0, width)
	y=random.randint(0, height)
	while running:
		key=pygame.key.get_pressed()
		mouse=pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		a=bot.segments[0]
		angle=math.degrees(math.atan2(a.ty-a.y, a.tx-a.x))
		if math.dist((x, y), (bot.segments[0].tx, bot.segments[0].ty))<15 or math.dist((x, y), (mouse[0], mouse[1]))<6:
			x=random.randint(0, width)
			y=random.randint(0, height)
		if key[pygame.K_m]:
			m=True
		if m:
			bot.move(x, y)
		pygame.draw.circle(window, (50, 0, 255), (x, y), 7)
		bot.draw(window)
		clear()
	pygame.quit()



if __name__ == "__main__":
	main()
