import pygame as pg
from random import shuffle

pg.init()

Window_size = (800, 800)
screen = pg.display.set_mode(Window_size)
pg.display.set_caption('Saper')

Black = (0, 0, 0)
Cian = (20, 137, 184)
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

#Сообщения проигрыша
FNT_number = pg.font.Font(pg.font.get_default_font(), 20)
FNT_text = pg.font.Font(pg.font.get_default_font(), 50)
FNT_restart = pg.font.Font(pg.font.get_default_font(), 50)
FNT_quit = pg.font.Font(pg.font.get_default_font(), 50)
FNT_start = pg.font.Font(pg.font.get_default_font(), 50)

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
			count -= 9
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

print(count_list)

game_menu = True
game_run = True
game_end = True

#Экран меню
spawn = 0
while game_menu:
	if spawn == 0:
		screen.fill(Gray)
		Saper_message = FNT_text.render("MineSwipper", True, Black)
		Start_message = FNT_restart.render("Start", True, Cian)
		quit1_message = FNT_quit.render("Quit", True, Black)
		Start_rect = Start_message.get_rect(topleft =(Window_size[0]//2-Window_size[0]//4, Window_size[1]//2-Window_size[1]//4 +80))
		quit1_message_rect = quit1_message.get_rect(topleft = (Window_size[0]//2-Window_size[0]//4, Window_size[1]//2-Window_size[1]//4 +160))
		screen.blit(Saper_message, (Window_size[0]//2-Window_size[0]//7, Window_size[1]//2-Window_size[1]//4))
		screen.blit(Start_message, Start_rect)
		screen.blit(quit1_message, quit1_message_rect)
		pg.display.flip()
		clock.tick(FPS)
		spawn += 1
	for event in pg.event.get():
		if event.type == pg.QUIT:
			game_run = False
			game_end = False
			game_menu = False
		if event.type == pg.MOUSEBUTTONDOWN:
			if quit1_message_rect.collidepoint(event.pos):
				game_run = False
				game_end = False
				game_menu = False
			if Start_rect.collidepoint(event.pos):
				screen.fill(Black)
				game_menu = False

#Экран игры
while game_run:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			game_end = False
			game_run = False
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				for i, index in enumerate(button_rects):
					if index.collidepoint(event.pos) and button_states[i]:
						button_states[i] = False
						pg.draw.rect(screen, Gray, index)
						number = FNT_number.render(str(count_list[i]), True, Black)
						screen.blit(number, index.center)
						if count_list[i] < 0:
							button_states = list(map(lambda x: False, button_states))
							game_run = False
													
						'''if count_list[i] == 0:
							button_states[i+1] = False #Право
							index.x += 40
							pg.draw.rect(screen, Gray, index)
							button_states[i-1] = False #Лево
							index.x -= 80
							pg.draw.rect(screen, Gray, index)
							button_states[i-19] = False #Верхняя left
							index.y -= 40
							pg.draw.rect(screen, Gray, index)
							button_states[i+21] = False #Нижняя left
							index.y += 80
							pg.draw.rect(screen, Gray, index)
							button_states[i+20] = False #Нижняя right
							index.x += 80
							pg.draw.rect(screen, Gray, index)
							button_states[i-20] = False #Верхняя right
							index.y -= 80
							pg.draw.rect(screen, Gray, index)
							button_states[i-21] = False #Верхняя
							index.x -= 40
							pg.draw.rect(screen, Gray, index)
							button_states[i+19] = False #Нижняя
							index.y += 80
							pg.draw.rect(screen, Gray, index)'''
			'''if event.button == 3:
				for i, index in enumerate(button_rects):
					if index.collidepoint(event.pos) and button_states[i]:
						flag_states[i] = False
						screen.blit(flag, index)'''
		
	for i, index in enumerate(copy_button_slice):
		if button_states[i]:
			screen.blit(bomb_image, index)

	for i, index in enumerate(button_rects):
		if button_states[i]: #and flag_states[i]:
			screen.blit(button_image, index)

	pg.display.flip()

	clock.tick(FPS)

#Экран проигрыша
if game_end:
	screen.fill(Gray)
	lose_message = FNT_text.render("You defeat!", True, Black)
	restart_label = FNT_restart.render("Restart", True, Cian)
	quit2_message = FNT_quit.render("Quit", True, Black)
	restart_label_rect = restart_label.get_rect(topleft =(Window_size[0]//2-Window_size[0]//4, Window_size[1]//2-Window_size[1]//4 +80))
	quit2_message_rect = quit2_message.get_rect(topleft = (Window_size[0]//2-Window_size[0]//4, Window_size[1]//2-Window_size[1]//4 +160))
	screen.blit(lose_message, (Window_size[0]//2-Window_size[0]//7, Window_size[1]//2-Window_size[1]//4))
	screen.blit(restart_label, restart_label_rect)
	screen.blit(quit2_message, quit2_message_rect)
	pg.display.flip()
	clock.tick(FPS)

while game_end:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			game_end = False
		if event.type == pg.MOUSEBUTTONDOWN:
			if quit2_message_rect.collidepoint(event.pos):
				game_end = False
			if restart_label_rect.collidepoint(event.pos):
				#Закинуть список бомб в функцию, закинуть счетчик в функцию, перезапустить их
				pass

pg.quit()