import pygame as pg
from random import shuffle

pg.init()

def Windows(Height, Width):
    Window_size = (Height, Width)
    screen = pg.display.set_mode(Window_size)
    pg.display.set_caption('Saper')
    return Window_size, screen
Window = Windows(800, 800)

Black = (0, 0, 0)
Cian = (20, 137, 184)
Gray = (180, 180, 180)

def Cell_quantity(Size):
    Cell_Qty = Size // 40
    return Cell_Qty #Кол-во полей в ряду
Cell = Cell_quantity(Window[0][0])

#Создание кнопки
original_button_image = pg.image.load("image/empty_button.png")
button_size = (40, 40)
button_image = pg.transform.scale(original_button_image, button_size)
button_rects = []

#Бомбы
original_bomb_image = pg.image.load("image/bomb.png")
bomb_size = (40, 40)
bomb_image = pg.transform.scale(original_bomb_image, bomb_size)

for row in range (Cell):
	for col in range (Cell):
		button_rect = pg.Rect(col * 40, row * 40, 40, 40)
		button_rects.append(button_rect)

button_states = [True] * len(button_rects)

#Добавление флага
original_flag = pg.image.load("image/flag.png")
flag_size = (40, 40)
flag = pg.transform.scale(original_flag, flag_size)
flag_states = [True] * len(button_rects)

#Сообщения проигрыша
FNT_number = pg.font.Font(pg.font.get_default_font(), 20)
FNT_text = pg.font.Font(pg.font.get_default_font(), Window[0][0]//20)
FNT_restart = pg.font.Font(pg.font.get_default_font(), Window[0][0]//20)
FNT_quit = pg.font.Font(pg.font.get_default_font(), Window[0][0]//20)
FNT_start = pg.font.Font(pg.font.get_default_font(), Window[0][0]//20)

def get_shuffled_slice(original_list):
    copy_list = original_list.copy()
    shuffle(copy_list)
    sliced_copy = copy_list[:int(len(original_list)*0.2)]
    return sliced_copy

clock = pg.time.Clock()
FPS = 10

def count_neighbors(original_list, sliced_list):
    count_list = []

    for index in original_list:
        count = 0
        x_coord, y_coord = index[0], index[1]

        for index_b in sliced_list:
            if [x_coord, y_coord] == [index_b[0], index_b[1]]:
                count -= 9
            if [x_coord, y_coord + 40] == [index_b[0], index_b[1]]:
                count += 1
            if [x_coord, y_coord - 40] == [index_b[0], index_b[1]]:
                count += 1
            if [x_coord + 40, y_coord] == [index_b[0], index_b[1]]:
                count += 1
            if [x_coord - 40, y_coord] == [index_b[0], index_b[1]]:
                count += 1
            if [x_coord + 40, y_coord + 40] == [index_b[0], index_b[1]]:
                count += 1
            if [x_coord + 40, y_coord - 40] == [index_b[0], index_b[1]]:
                count += 1
            if [x_coord - 40, y_coord + 40] == [index_b[0], index_b[1]]:
                count += 1
            if [x_coord - 40, y_coord - 40] == [index_b[0], index_b[1]]:
                count += 1

        count_list.append(count)

    return count_list

game_menu = True
game_run = True
game_end = True

def run_game(button_rects, button_states, copy_button_slice, count_list, bomb_image, button_image, FPS, Gray, Black, FNT_number, flag_states, flag, screen):
    global game_run
    global game_end
    global clock

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
                                screen.blit(bomb_image, index)
                                button_states = list(map(lambda x: False, button_states))
                                game_run = False
                if event.button == 3:
                    for i, index in enumerate(button_rects):
                        if index.collidepoint(event.pos) and button_states[i]:
                            if flag_states[i] == False:
                                flag_states[i] = True
                            else:
                                flag_states[i] = False
                                screen.blit(flag, index)

        for i, index in enumerate(button_rects):
            if button_states[i] and flag_states[i]:
                screen.blit(button_image, index)

        pg.display.flip()
        clock.tick(FPS)

spawn = 0
while game_menu:
    if spawn == 0:
        Window[1].fill(Gray)
        Saper_message = FNT_text.render("MineSwipper", True, Black)
        Start_message = FNT_restart.render("Start", True, Cian)
        Setting_message = FNT_text.render("Setting", True, Black)
        quit1_message = FNT_quit.render("Quit", True, Black)
        Start_rect = Start_message.get_rect(topleft =(Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +40))
        #Настройки
        Setting_message_rect = Setting_message.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +80))
        #Сложность
        Complexity = FNT_text.render("Complexity:", True, Black)
        light = FNT_text.render("Light", True, Black)
        medium = FNT_text.render("Medium", True, Black)
        hard = FNT_text.render("Hard", True, Black)
        #Музыка
        Music = FNT_text.render("Light", True, Black)
        #Назад
        Back = FNT_text.render("Back", True, Black)
        #
        Complexity_rect = Complexity.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +40))
        light_rect = light.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4 + 20, Window[0][1]//2-Window[0][1]//4 +80))
        medium_rect = medium.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4 +20, Window[0][1]//2-Window[0][1]//4 +120))
        hard_rect = hard.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4+20, Window[0][1]//2-Window[0][1]//4 +160))
        Back_rect = Back.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +200))
		##################
        quit1_message_rect = quit1_message.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +120))
        Window[1].blit(Saper_message, (Window[0][0]//2-Window[0][0]//7, Window[0][1]//2-Window[0][1]//4))
        Window[1].blit(Start_message, Start_rect)
        Window[1].blit(Setting_message, Setting_message_rect)
        Window[1].blit(quit1_message, quit1_message_rect)
        pg.display.flip()
        clock.tick(FPS)
        spawn += 1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_run = False
            game_end = False
            game_menu = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if quit1_message_rect.collidepoint(event.pos):
                    game_run = False
                    game_end = False
                    game_menu = False
                if Start_rect.collidepoint(event.pos):
                    copy_button_slice_c = get_shuffled_slice(button_rects)
                    count_list_c = count_neighbors(button_rects, copy_button_slice_c)
                    run_game(button_rects, button_states, copy_button_slice_c, count_list_c, bomb_image, button_image, FPS, Gray, Black, FNT_number, flag_states, flag, Window[1])
                    game_menu = False
                if Setting_message_rect.collidepoint(event.pos):
                    Window[1].fill(Gray)
                    Window[1].blit(Setting_message, (Window[0][0]//2-Window[0][0]//7, Window[0][1]//2-Window[0][1]//4))
                    Window[1].blit(Complexity, Complexity_rect)
                    Window[1].blit(light, light_rect)
                    Window[1].blit(medium, medium_rect)
                    Window[1].blit(hard, hard_rect)
                    Window[1].blit(Back, Back_rect)
                    wait = 0
                    pg.display.flip()
                    while wait == 0:
                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                game_run = False
                                game_end = False
                                game_menu = False
                                wait += 1
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    if light_rect.collidepoint(event.pos):
                                        Window = Windows(360, 360)
                                        Cell = Cell_quantity(Window[0][0])
                                        spawn = 0
                                        wait += 1
                                    if medium_rect.collidepoint(event.pos):
                                        Window = Windows(600, 600)
                                        Cell = Cell_quantity(Window[0][0])
                                        spawn = 0
                                        wait += 1
                                    if hard_rect.collidepoint(event.pos):
                                        Window = Windows(800, 800)
                                        Cell = Cell_quantity(Window[0][0])
                                        spawn = 0
                                        wait += 1
                                        
eteration = 1
while game_end:
    if eteration == 1:
        count_spawn = 0
        if count_spawn == 0:
            Window[1].fill(Gray)
            lose_message = FNT_text.render("You defeat!", True, Black)
            restart_label = FNT_restart.render("Restart", True, Cian)
            quit2_message = FNT_quit.render("Quit", True, Black)
            restart_label_rect = restart_label.get_rect(topleft =(Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +40))
            quit2_message_rect = quit2_message.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +80))
            Window[1].blit(lose_message, (Window[0][0]//2-Window[0][0]//7, Window[0][1]//2-Window[0][1]//4))
            Window[1].blit(restart_label, restart_label_rect)
            Window[1].blit(quit2_message, quit2_message_rect)
            pg.display.flip()
            clock.tick(FPS)

    eteration += 1

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_end = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if quit2_message_rect.collidepoint(event.pos):
                    game_end = False
                if restart_label_rect.collidepoint(event.pos):
                    Window[1].fill(Black)
                    eteration = 1
                    button_states = list(map(lambda x: True, button_states))
                    flag_states = list(map(lambda x: True, flag_states))
                    game_run = True
                    copy_button_slice_c = get_shuffled_slice(button_rects)
                    count_list_c = count_neighbors(button_rects, copy_button_slice_c)
                    run_game(button_rects, button_states, copy_button_slice_c, count_list_c, bomb_image, button_image, FPS, Gray, Black, FNT_number, flag_states, flag, Window[1])

pg.quit()