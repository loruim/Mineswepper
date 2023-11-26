import pygame as pg
import random

#from pygame.sprite import _Group

pg.init()

Window_size = (800, 800)
screen = pg.display.set_mode(Window_size)
pg.display.set_caption('Saper')

#Создание кнопки
original_button_image = pg.image.load("image/empty_button.png")
button_size = (40, 40)
button_image = pg.transform.scale(original_button_image, button_size)
button_rects = []

clock = pg.time.Clock()
FPS = 10

Black = (0, 0, 0)
Gray = (180, 180, 180)
screen.fill(Gray)

Cell_Qty = 20 #Кол-во полей в ряду

FNT18 = pg.font.Font(pg.font.get_default_font(), 20)

for row in range (Cell_Qty):
	for col in range (Cell_Qty):
		button_rect = pg.Rect(col * button_size[0], row * button_size[1], *button_size)
		button_rects.append(button_rect)
'''for row in range(Cell_Qty): #Для каждого ряда
	button_rect.y = row
	for colum in range(Cell_Qty):
		#create | draw cell
		cell = pg.Surface((Cell_size, Cell_size)) # Create Cells
		cell.fill(Gray)
		screen.blit(cell, (colum*Cell_size, row*Cell_size)) # Draw Cells
		pg.draw.rect(screen, Black, (colum*Cell_size, row*Cell_size, Cell_size, Cell_size), 1)
		#Create | draw number
		number = FNT18.render(str(random.randint(0, 5)), 1, Black)
		screen.blit(number, (colum*Cell_size+Cell_Qty//2, row*Cell_size+Cell_Qty//2))
			'''

for index in button_rects:
	screen.blit(button_image, index)

run = True
while run:
	pg.display.update()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			run = False
		'''if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				number = FNT18.render(str(random.randint(0, 5)), 1, Black)
				screen.blit(number, (event.pos[0], event.pos[1]))'''
	clock.tick(FPS)
