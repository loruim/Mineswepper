import pygame as pg
import random 
from random import shuffle

#from pygame.sprite import _Group

pg.init()

Window_size = (800, 800)
screen = pg.display.set_mode(Window_size)
pg.display.set_caption('Saper')

FNT18 = pg.font.Font(pg.font.get_default_font(), 20)
Black = (0, 0, 0)
Gray = (180, 180, 180)

Cell_Qty = 20 #Кол-во полей в ряду

#Создание кнопки
original_button_image = pg.image.load("image/empty_button.png")
button_size = (Window_size[0]/Cell_Qty, Window_size[1]/Cell_Qty)
button_image = pg.transform.scale(original_button_image, button_size)
button_rects = []

for row in range (Cell_Qty):
	for col in range (Cell_Qty):
		button_rect = pg.Rect(col * button_size[0], row * button_size[1], *button_size)
		button_rects.append(button_rect)

button_states = [True] * len(button_rects)

clock = pg.time.Clock()
FPS = 10

run = True
while run:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = False
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				for i, index in enumerate(button_rects):
					if index.collidepoint(event.pos) and button_states[i]:
						button_states[i] = False
						pg.draw.rect(screen, Gray, index)
						number = FNT18.render(str(random.randint(0, 8)), True, Black)
						screen.blit(number, index.center)
				

	for i, index in enumerate(button_rects):
		if button_states[i]:
			screen.blit(button_image, index)

	pg.display.flip()

	clock.tick(FPS)

pg.quit()

