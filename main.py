from logics import * # здесь все функции хранятся
import pygame, sys
from database import get_best_score, cursor, insert_result # работа с таблицей игроков (БД sqlite)

# константы_______________________________________
RANGE_MAS = 4 # размер матрицы, не может быть меньше 1 (будут ошибки)
# параметры графического окна
SIZE_BLOCK = 110 # размер квадрата
MARGIN = 10 # отступы между квадратами
WIDTH = RANGE_MAS * SIZE_BLOCK + (RANGE_MAS + 1) * MARGIN # общая ширина графического окна
TITLE = 110 # размер заголовка со счетом
HEIGTH = WIDTH + TITLE # общая высота графического окна
TITLE_RECT = pygame.Rect(0, 0, WIDTH, TITLE)
COLOR_TITLE = (255, 255, 255) # белый
COLOR_VALUE = (0, 0, 0) # черный
BLACK = (0, 0, 0) # черный для заливки/обновления экрана
COLOR_TEXT = (255, 127, 0) # оранжевый для основного текста
COLOR_DELTA = 'blue' # синий для изменения счета

# цветовая схема квадратов игры
COLORS = {
	0: (130, 130, 130),
	2: (255, 255, 255),
	4: (255, 255, 128),
	8: (255, 255, 0),
	16: (255, 200, 255),
	32: (255, 200, 128),
	64: (255, 200, 0),
	128: (255, 150, 255),
	256: (255, 150, 128),
	512: (255, 150, 0),
	1024: (255, 100, 255),
	2048: (255, 100, 128)
}
GAMERS_DB = get_best_score() # tuple с лучшими игроками их счетом
USERNAME = None # Имя пользователя
mas = None # матрица квадратов
score = None # количество очков

# функции_______________________________________

# инициализация начальных значений
def init_const():
	global score, mas
	score = 0 # количество очков
	# начальные настройки
	# матрица нулей размером RANGE_MAS х RANGE_MAS
	mas = [[0 for _ in range(RANGE_MAS)] for _ in range(RANGE_MAS)]
	# положим в массив два значения
	empty = get_empty_list(mas, RANGE_MAS)
	random.shuffle(empty) # перемешаем пустые номера
	for _ in range(2):
		random_num = empty.pop() # вернем последний элемент, через удаление :)
		row, column = get_index_from_number(random_num, RANGE_MAS) # получим координаты этого номера
		mas = insert_2_or_4(mas, row, column) # добавим 2 или 4 в нашу "случайную ячейку"


# выводит начальную заставку и запрашивает имя игрока
def draw_intro():
	greeting = 'Enter your name'
	name = greeting
	enter_name = False

	try: # мало ли, вдруг картинки не будет
		img_logo = pygame.image.load('logo.png') # логотип
	except:
		img_logo = None

	while not enter_name:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # нажали на крестик "x"
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.KEYDOWN: # любая другая кнопка
				if event.unicode.isalpha(): # это буква
					if name == greeting:
						name = event.unicode
					else:
						name += event.unicode
				elif event.key == pygame.K_BACKSPACE: # удаление последней буквы
					name = name[: -1]
				elif event.key == pygame.K_RETURN: # Enter
					if len(name) > 2:
						global USERNAME
						USERNAME = name
						enter_name = True
						break

		screen.fill(BLACK) # закрасим все что есть черным
		text_name = FONT_NAME.render(name, True, COLOR_TEXT)
		rect_name = text_name.get_rect() # узнаем размер текста
		rect_name.center = screen.get_rect().center # располагаем по центру

		if img_logo is not None:
			screen.blit(pygame.transform.scale(img_logo, [SIZE_BLOCK * 2, SIZE_BLOCK * 2]), [MARGIN, MARGIN]) # размер картинки

		screen.blit(TEXT_WELLCOME, (SIZE_BLOCK * 2 + MARGIN * 2, MARGIN * 8))
		screen.blit(text_name, rect_name)
		pygame.display.update() # обновим изменения графики

	screen.fill(BLACK) # обновим экран


# выводит конечную заставку, счет игрока и записывает данные в БД SQLite
def draw_game_over():
	global USERNAME

	screen.fill(BLACK) # закрасим все что есть черным

	try: # мало ли, вдруг картинки не будет
		img_logo = pygame.image.load('gameover.jpg') # логотип
		screen.blit(pygame.transform.scale(img_logo, [SIZE_BLOCK * 2, SIZE_BLOCK * 2]), [MARGIN, MARGIN]) # размер картинки
	except:
		pass
	
	screen.blit(TEXT_GAME_OVER, (SIZE_BLOCK * 2 + MARGIN * 2, MARGIN * 8))

	if GAMERS_DB:
		best_score = GAMERS_DB[0][1]
	else:
		best_score = 0 # БД пустая

	if score > best_score: # был поставлен рекорд
		text = "Record broken!"
	else:
		text = f"Record {best_score}"

	text_score = FONT_NAME.render(f"Your score {score}", True, COLOR_TEXT)
	screen.blit(text_score, (MARGIN *3, HEIGTH // 2))
	text_record = FONT_NAME.render(text, True, COLOR_TEXT)
	screen.blit(text_record, (MARGIN *3, HEIGTH // 2 + SIZE_BLOCK // 2))

	# пробел - еще раз, enter - новая игра
	text_space = FONT_SCORE.render("<Space> try again", True, COLOR_TEXT)
	text_enter = FONT_SCORE.render("<Enter> new gamer", True, COLOR_TEXT)
	screen.blit(text_space, (MARGIN *3, HEIGTH - MARGIN * 9))
	screen.blit(text_enter, (MARGIN *3, HEIGTH - MARGIN * 5))
	
	pygame.display.update() # обновим изменения графики	
	insert_result(USERNAME, score) # запишем результат в БД
	
	make_disicion = False # приняли решение в конце игры?
	while not make_disicion:
		for event in pygame.event.get(): # опрос событий (нажатие кнопок и т.п.)
			if event.type == pygame.QUIT: # нажали на крестик "x"
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.KEYDOWN: # любая другая кнопка
				if event.key == pygame.K_RETURN: # Enter
					# перезапускаем игру с новым игроком
					USERNAME = None
					make_disicion = True
				elif event.key == pygame.K_SPACE: # пробел
					# перезапускаем игру с этим же именем
					make_disicion = True

	screen.fill(BLACK) # закрасим все что есть черным


# выводит лучших игроков и их счет
def draw_top_gamers():
	screen.blit(TEXT_HEAD, (SIZE_BLOCK * 2.5, MARGIN - 5))
	for index, gamer in enumerate(GAMERS_DB): # возвращаем значения с индексом, чтобы место знать
		name, score = gamer # распакуем tuple
		text = f"{index + 1}. {name} - {score}"
		text_gamer = FONT_GAMER.render(text, True, COLOR_TEXT)
		screen.blit(text_gamer, (SIZE_BLOCK * 2.5, MARGIN * 3 + MARGIN * 2 * index))


# отрисовка графики. в logics.py не помещаем, т.к. нужны доступы к screen
# чтобы не усложнять не будем передавать screen, а реализуем функцию в этом модуле
def draw_interface(score = 0, delta = 0):
	pretty_print(mas) # вывод трассировки
	# рисуем графическое окно
	pygame.draw.rect(screen, COLOR_TITLE, TITLE_RECT)
	text_score_value = FONT_SCORE.render(f'{score}', True, COLOR_TEXT)
	screen.blit(TEXT_SCORE, (SIZE_BLOCK // 5, TITLE // 3))
	screen.blit(text_score_value, (SIZE_BLOCK * 1.5 , TITLE // 3))

	if delta > 0: # вывод изменения счета
		text_delta = FONT_DELTA.render(f'+{delta}', True, COLOR_DELTA)
		screen.blit(text_delta, (SIZE_BLOCK * 1.5 - MARGIN , TITLE // 2 + 10))

	draw_top_gamers()

	for row in range(RANGE_MAS):
		for column in range(RANGE_MAS):
			# отрисовка квадратов
			w = column * SIZE_BLOCK + (column + 1) * MARGIN
			h = row * SIZE_BLOCK + (row + 1) * MARGIN + TITLE
			value = mas[row][column]
			pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))

			# отрисовка значений в ячейках
			if value != 0:
				text = FONT.render(f'{value}', True, COLOR_VALUE)
				font_w, font_h = text.get_size() # узнаем размер текста
				# найдем координаты для вывода текста по середине
				text_x = w + (SIZE_BLOCK - font_w) / 2
				text_y = h + (SIZE_BLOCK - font_h) / 2
				screen.blit(text, (text_x, text_y)) # вывод текста

	pygame.display.update() # обновим изменения графики


# игровой цикл
def game_loop():
	global score, mas # ссылаемся на глобальные переменные

	draw_interface(score) # графическое окно игры
	# начало цикла игры_______________________________________
	# если пустых клеток нет и нельзя двигать массив, то игра закончена
	while is_zero_in_mas(mas) or can_move(mas,  RANGE_MAS):
		# break # это для теста команда
		# обработчик событий в pygame
		# ждать от пользователя команды
		# когда получим команду - обработать массив (делаем через pygame, пока на паузе)	
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # нажали на крестик "x"
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.KEYDOWN: # любая другая кнопка
				
				delta = 0

				if event.key == pygame.K_LEFT:
					mas, delta = move_left(mas, RANGE_MAS)
				elif event.key == pygame.K_RIGHT:
					mas, delta = move_right(mas, RANGE_MAS)
				elif event.key == pygame.K_UP:
					mas, delta = move_up(mas, RANGE_MAS)
				elif event.key == pygame.K_DOWN:
					mas, delta = move_down(mas, RANGE_MAS)
				else: # на другие кнопки не реагируем
					continue

				score += delta			

				# найти пустые клетки
				# если есть пустые клетки, случайно выбрать одну из них
				# и положить туда либо 2, либо 4
				if is_zero_in_mas(mas): # т.е. есть еще пустые ячейки
					empty = get_empty_list(mas, RANGE_MAS)
					random.shuffle(empty) # перемешаем пустые номера
					random_num = empty.pop() # вернем последний элемент, через удаление :)
					row, column = get_index_from_number(random_num, RANGE_MAS) # получим координаты этого номера
					mas = insert_2_or_4(mas, row, column) # добавим 2 или 4 в нашу "случайную ячейку"
					print(f'заполнили элемент по номером {random_num}')
		
				draw_interface(score, delta) # обновим счет


# основная программа_______________________________________

# настроим графическое окно игры
pygame.init()
FONT = pygame.font.SysFont("stxingkai", 70) # шрифт цифр в квадрате
FONT_SCORE = pygame.font.SysFont("simsun", 48) # шрифт счета (score) в заголовке
FONT_DELTA = pygame.font.SysFont("simsun", 32) # шрифт для delta изменения счета
FONT_TOP = pygame.font.SysFont("simsun", 30) # шрифт счета лучших игроков
TEXT_HEAD = FONT_TOP.render("Bests", True, COLOR_TEXT) # заголовок лучших
FONT_GAMER = pygame.font.SysFont("simsun", 24) # шрифт имен лучших игроков
TEXT_SCORE = FONT_SCORE.render("Score: ", True, COLOR_TEXT) # заголовок счета
FONT_WELLCOME = pygame.font.SysFont("stxingkai", 70) # шрифт приветствия
TEXT_WELLCOME = FONT_WELLCOME.render("Wellcome!", True, COLOR_TEXT) # приветствие intro
TEXT_GAME_OVER = FONT_WELLCOME.render("oops.. :(", True, COLOR_TEXT) # приветствие game over
FONT_NAME = pygame.font.SysFont("stxingkai", 70) # шрифт запроса имени
screen = pygame.display.set_mode((WIDTH, HEIGTH)) # основное окно игры
pygame.display.set_caption("game 2048") # заголовок окна

# начинаем игру ___________________________________
while True:
	
	init_const() # обнуление счета и матрицы

	if USERNAME is 	None:
		draw_intro() # начальная заставка и запрос имени игрока

	game_loop() # игра
	draw_game_over() # конечная заставка


# end

