import pygame as pg
import time
from random import shuffle

pg.init()

def Windows(Height, Width):
    """Создает и возвращает размеры окна по высоте Height и ширине Width, также создает и возвращает поверхность screen
    :param Height: height
    :type Height: int
    :param Width: width
    :type Width: int
    :results Window_size: tuple of Height and Width
    :rtype Window_size: tuple
    :result screen: visible field
    :rtype screen: pygame.surface.Surface"""
    Window_size = (Height, Width)
    screen = pg.display.set_mode(Window_size)
    pg.display.set_caption('Saper')
    return Window_size, screen
Window = Windows(800, 800)

Black = (0, 0, 0)
Cian = (20, 137, 184)
Gray = (180, 180, 180)

def Cell_quantity(Size):
    """Возвращает количество клеток в ряду/стобце
    :param Size: size window
    :type Size: int
    :returns: integer division of Size by cell length/width
    :rtype: int"""
    Cell_Qty = Size // 40
    return Cell_Qty

#Создание кнопки
original_button_image = pg.image.load("image/empty_button.png")
button_size = (40, 40)
button_image = pg.transform.scale(original_button_image, button_size)

#Бомбы
original_bomb_image = pg.image.load("image/bomb.png")
bomb_size = (40, 40)
bomb_image = pg.transform.scale(original_bomb_image, bomb_size)

def number_spawn(Cells):
    """Создает каждую кнопку как обьект Rect, после помещает эти кнопки в список button_rects и возвращает его, создает два списка длиной button_rects со значениями True
    :param Cells: number of cells
    :type Cells: int
    :returns button_rects: list Cells*Cells with button coordinates
    :rtype button_rects: list
    :returns button_states: list [True] Cells*Cells
    :rtype button_states: list
    :returns flag_states: list [True] Cells*Cells
    :rtype flag_states: list"""
    button_rects = []
    for row in range (Cells):
        for col in range (Cells):
            button_rect = pg.Rect(col * 40, row * 40, 40, 40)
            button_rects.append(button_rect)
    button_states = [True] * len(button_rects)
    flag_states = [True] * len(button_rects)
    return button_rects, button_states, flag_states

#Добавление флага
original_flag = pg.image.load("image/flag.png")
flag_size = (40, 40)
flag = pg.transform.scale(original_flag, flag_size)

#Сообщения проигрыша
FNT_number = pg.font.Font(pg.font.get_default_font(), 20)
FNT = pg.font.Font(pg.font.get_default_font(), Window[0][0]//20)

def get_shuffled_slice(original_list):
    """Создает копию кортежа с координатами кнопок, перемешивает его и уберает 80% последних значений - это мины, также определяет количество клеток не являющихся минами
    :param original_list: cell coordinates
    :type original_list: list
    :returns sliced_copy: 20% of mixed original_list
    :rtype sliced_copy: list
    :returns not_minus: length original_list - length sliced_copy
    :rtype not_minus: int"""
    copy_list = original_list.copy()
    shuffle(copy_list)
    sliced_copy = copy_list[:int(len(original_list)*0.2)]
    not_minus = len(original_list) - len(sliced_copy)
    return sliced_copy, not_minus

clock = pg.time.Clock()
FPS = 10

def count_neighbors(original_list, sliced_list):
    """Считает количество мин вокруг клеток, если клетка и есть мина, присваевает ей отрицательное значение
    :param original_list: cell coordinates
    :type original_list: list
    :param sliced_list: 20% of mixed original_list
    :type sliced_list: list
    :returns: number for each cell
    :rtype: list"""
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
game_win = False
Winner_state = []

def run_game(button_rects, button_states, not_minus, count_list, bomb_image, button_image, FPS, Gray, Black, FNT_number, flag_states, flag, screen):
    """Основной цикл игры - генерация клеток, цифр, бомб, также проверка условий победы и запись отчета при победе
    :param button_rects: cell coordinates
    :type button_rects: list
    :param button_states: index of each cell
    :type button_states: list
    :param not_minus: quantity not min
    :type not_minus: int
    :param count_list: number for each cell
    :type count_list: list
    :param bomb_image: image
    :type bomb_image: pygame.surface.Surface
    :param button_image: image
    :type button_image: pygame.surface.Surface
    :param FPS: number of frames per second
    :type FPS: int
    :param Gray: color
    :type Gray: tuple
    :param Black: color
    :type Black: tuple
    :param FNT_number: font
    :type FNT_number: pygame.font.Font
    :param flag_states: index of each flag
    :type flag_states: list
    :param flag: image
    :type flag: pygame.surface.Surface
    :param screen: visible field
    :type screen: pygame.surface.Surface"""
    global game_run
    global game_end
    global game_win
    global clock
    global Winner_state
    start_time = time.time()

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
                            if button_states[i] == False and count_list[i] >= 0:
                                Winner_state.append(0)
                                if len(Winner_state) == not_minus:
                                    game_win = True
                                    game_end = False
                                    end_time = time.time()
                                    execution_time = end_time - start_time
                                    with open("result.txt", "a") as f:
                                        if len(button_rects) == 81:
                                            f.write(f"game\ngame time - {execution_time}\nComplexity - light")
                                        if len(button_rects) == 255:
                                            f.write(f"game number\ngame time - {execution_time}\nComplexity - middle")
                                        if len(button_rects) == 400:
                                            f.write(f"game number\ngame time - {execution_time}\nComplexity - hard")
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
        Saper_message = FNT.render("MineSwipper", True, Black)
        Start_message = FNT.render("Start", True, Cian)
        Setting_message = FNT.render("Setting", True, Black)
        quit1_message = FNT.render("Quit", True, Black)
        history = FNT.render("History", True, Black)
        Start_rect = Start_message.get_rect(topleft =(Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +40))
        history_rect = history.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +80))
        #Настройки
        Setting_message_rect = Setting_message.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +120))
        #Сложность
        Complexity = FNT.render("Complexity:", True, Black)
        light = FNT.render("Light", True, Black)
        medium = FNT.render("Medium", True, Black)
        hard = FNT.render("Hard", True, Black)
        #Назад
        Back = FNT.render("Back", True, Black)
        #
        Complexity_rect = Complexity.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +40))
        light_rect = light.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4 + 20, Window[0][1]//2-Window[0][1]//4 +80))
        medium_rect = medium.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4 +20, Window[0][1]//2-Window[0][1]//4 +120))
        hard_rect = hard.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4+20, Window[0][1]//2-Window[0][1]//4 +160))
        Back_rect = Back.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +200))
		##################
        quit1_message_rect = quit1_message.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +160))
        Window[1].blit(Saper_message, (Window[0][0]//2-Window[0][0]//7, Window[0][1]//2-Window[0][1]//4))
        Window[1].blit(Start_message, Start_rect)
        Window[1].blit(Setting_message, Setting_message_rect)
        Window[1].blit(history, history_rect)
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
                    Cell = Cell_quantity(Window[0][0])
                    number = number_spawn(Cell)
                    copy_button_slice_c = get_shuffled_slice(number[0])
                    count_list_c = count_neighbors(number[0], copy_button_slice_c[0])
                    run_game(number[0], number[1], copy_button_slice_c[1], count_list_c, bomb_image, button_image, FPS, Gray, Black, FNT_number, number[2], flag, Window[1])
                    game_menu = False
                if history_rect.collidepoint(event.pos):
                    with open("result.txt", "r") as f:
                        content = f.read()
                        print(content)
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
                                    if Back_rect.collidepoint(event.pos):
                                        spawn = 0
                                        wait += 1
                                    if light_rect.collidepoint(event.pos):
                                        Window = Windows(360, 360)
                                        Cell = Cell_quantity(Window[0][0])
                                        number = number_spawn(Cell)
                                        spawn = 0
                                        wait += 1
                                    if medium_rect.collidepoint(event.pos):
                                        Window = Windows(600, 600)
                                        Cell = Cell_quantity(Window[0][0])
                                        number = number_spawn(Cell)
                                        spawn = 0
                                        wait += 1
                                    if hard_rect.collidepoint(event.pos):
                                        Window = Windows(800, 800)
                                        Cell = Cell_quantity(Window[0][0])
                                        number = number_spawn(Cell)
                                        spawn = 0
                                        wait += 1
                                        
eteration = 1
while game_end:
    if eteration == 1:
        Window[1].fill(Gray)
        lose_message = FNT.render("You defeat!", True, Black)
        restart_label = FNT.render("Restart", True, Cian)
        quit2_message = FNT.render("Quit", True, Black)
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
                    game_run = True
                    Cell = Cell_quantity(Window[0][0])
                    number = number_spawn(Cell)
                    copy_button_slice_c = get_shuffled_slice(number[0])
                    count_list_c = count_neighbors(number[0], copy_button_slice_c[0])
                    Winner_state = []
                    run_game(number[0], number[1], copy_button_slice_c[1], count_list_c, bomb_image, button_image, FPS, Gray, Black, FNT_number, number[2], flag, Window[1])

while game_win:
    if eteration == 1:
        Window[1].fill(Gray)
        Win_message = FNT.render("You WIN!", True, Black)
        new_game_label = FNT.render("New game", True, Cian)
        quit3_message = FNT.render("Quit", True, Black)
        new_game_label_rect = new_game_label.get_rect(topleft =(Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +40))
        quit3_message_rect = quit3_message.get_rect(topleft = (Window[0][0]//2-Window[0][0]//4, Window[0][1]//2-Window[0][1]//4 +80))
        Window[1].blit(Win_message, (Window[0][0]//2-Window[0][0]//7, Window[0][1]//2-Window[0][1]//4))
        Window[1].blit(new_game_label, new_game_label_rect)
        Window[1].blit(quit3_message, quit3_message_rect)
        pg.display.flip()
        clock.tick(FPS)

    eteration += 1

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_win = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if quit3_message_rect.collidepoint(event.pos):
                    game_win = False
                if new_game_label_rect.collidepoint(event.pos):
                    Window[1].fill(Black)
                    eteration = 1
                    game_run = True
                    Cell = Cell_quantity(Window[0][0])
                    number = number_spawn(Cell)
                    copy_button_slice_c = get_shuffled_slice(number[0])
                    count_list_c = count_neighbors(number[0], copy_button_slice_c[0])
                    Winner_state = []
                    run_game(number[0], number[1], copy_button_slice_c[1], count_list_c, bomb_image, button_image, FPS, Gray, Black, FNT_number, number[2], flag, Window[1])

pg.quit()