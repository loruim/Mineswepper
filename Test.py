import pygame as pg
from random import shuffle

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

#Бомбы
original_bomb_image = pg.image.load("image/bomb.png")
bomb_size = (Window_size[0]/Cell_Qty, Window_size[1]/Cell_Qty)
bomb_image = pg.transform.scale(original_bomb_image, bomb_size)

for row in range (Cell_Qty):
	for col in range (Cell_Qty):
		button_rect = pg.Rect(col * button_size[0], row * button_size[1], *button_size)
		button_rects.append(button_rect)

button_states = [True] * len(button_rects)

#Добавление флага
original_flag = pg.image.load("image/flag.png")
flag_size = (Window_size[0]/Cell_Qty, Window_size[1]/Cell_Qty)
flag = pg.transform.scale(original_flag, flag_size)
flag_states = [True] * len(button_rects)

copy_button_rects = button_rects.copy()
shuffle(copy_button_rects)
copy_button_slice = copy_button_rects[:int(len(button_rects)*0.2)]

clock = pg.time.Clock()
FPS = 10

count_list =[]
for index in button_rects:
	count = 0
	x_coord = index[0]
	y_coord = index[1]
	for index_b in copy_button_slice:
		if [x_coord, y_coord] == [index_b[0], index_b[1]]:
			pass
		if [x_coord, y_coord+40] == [index_b[0], index_b[1]]: #Снизу
			count += 1
		if [x_coord, y_coord-40] == [index_b[0], index_b[1]]: #Сверху
			count += 1
		if [x_coord+40, y_coord] == [index_b[0], index_b[1]]: #Справа
			count += 1
		if [x_coord-40, y_coord] == [index_b[0], index_b[1]]: #Слева
			count += 1
		if [x_coord+40, y_coord+40] == [index_b[0], index_b[1]]: #Правый нижний угол
			count += 1
		if [x_coord+40, y_coord-40] == [index_b[0], index_b[1]]: #Правый верхний угол
			count += 1
		if [x_coord-40, y_coord+40] == [index_b[0], index_b[1]]: #Левый нижний угол
			count += 1
		if [x_coord-40, y_coord-40] == [index_b[0], index_b[1]]: #Левый верхний угол
			count += 1
	count_list.append(count)

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
						number = FNT18.render(str(count_list[i]), True, Black)
						screen.blit(number, index.center)
			if event.button == 3:
				for i, index in enumerate(button_rects):
					if index.collidepoint(event.pos) and button_states[i]:
						screen.blit(flag, index)
						flag_states[i] = False
				
	for i, index in enumerate(copy_button_slice):
		if flag_states[i]:
			screen.blit(bomb_image, index)

	for i, index in enumerate(button_rects):
		if button_states[i] and flag_states[i]:
			screen.blit(button_image, index)

	pg.display.flip()

	clock.tick(FPS)

pg.quit()