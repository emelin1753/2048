import random

# функция красиво распечатает матрицу
def pretty_print(mas):
	print('-' * 10) # 10 раз тире
	[print(*row) for row in mas] # оператор '*' делает распаковку списка, без запятых и квадратных скобок 
	print('-' * 10) # 10 раз тире


# функция по номеру строки и столбца вернет порядковый номер ячейки от 1 до 16 по формуле (i * range_of_mas + j + 1)
def get_number_from_index(row, column, range_of_mas):
	return row * range_of_mas + column + 1


# функция возвращает случайное число из диапазона a, b
def rand_int(a, b):
	return random.randint(a, b)


# функция по порядковому номеру вернет коррдинаты (индексы). фукнция обратная предыдущей
def get_index_from_number(num, range_of_mas):
	num -= 1 # сначала уменьшаем на 1
	row, column = num // range_of_mas, num % range_of_mas # делим нацело, берем остаток от деления
	return row, column


# функция вставит 2 или 4 в матрицу
def insert_2_or_4(mas, row, column):
	if random.random() <= 0.75:
		mas[row][column] = 2 # двойка будет выпадать чаще
	else:	
		mas[row][column] = 4
	return mas


# функция проверяет есть ли свободные (нулевые) ячейки
def is_zero_in_mas(mas):
	for row in mas:
		if 0 in row:
			return True
	return False


# функция определяет пустые клетки, в которые мы будем помещать 2 или 4
def get_empty_list(mas, range_of_mas):
	# перебираем все значения из матрицы по строкам и столбцам
	# ищем только нулевые (свободные ячейки)
	# в виде list comprehension
	empty = [get_number_from_index(row, column, range_of_mas) for row in range(range_of_mas) for column in range(range_of_mas) if mas[row][column] == 0]
	return empty


# двигаем ячейки влево и схлопываем
def move_left(mas, range_of_mas):
	delta = 0 # для подсчета очков
	# сместим влево без схлопвыания (т.е. убираем промежуточные нули)
	for row in mas:
		while 0 in row:
			row.remove(0) # удаляем нули
		while len(row) < range_of_mas:
			row.append(0) # добавим нули в конец
	
	for row in range(range_of_mas):
		for column in range(range_of_mas - 1):
			if mas[row][column] == mas[row][column + 1] and mas[row][column] != 0: # тогда схлопываем
				mas[row][column] *= 2 # хлоп!
				delta += mas[row][column] # увеличим количество очков
				mas[row].pop(column + 1) # удаляем соседа справа
				mas[row].append(0) # добавляем 0 в конец ряда

	return mas, delta


# двигаем ячейки вправо и схлопываем
def move_right(mas, range_of_mas):
	delta = 0 # для подсчета очков
	# сместим вправо без схлопвыания (т.е. убираем промежуточные нули)
	for row in mas:
		while 0 in row:
			row.remove(0) # удаляем нули
		while len(row) < range_of_mas:
			row.insert(0, 0) # добавим нули в начало
	
	for row in range(range_of_mas):
		for column in range(range_of_mas - 1, 0, -1):
			if mas[row][column] == mas[row][column - 1] and mas[row][column] != 0: # тогда схлопываем
				mas[row][column] *= 2 # хлоп!
				delta += mas[row][column] # увеличим количество очков
				mas[row].pop(column - 1) # удаляем соседа слева
				mas[row].insert(0, 0) # добавляем 0 в начало ряда

	return mas, delta


# двигаем ячейки вверх и схлопываем
def move_up(mas, range_of_mas):
	delta = 0 # для подсчета очков
	for j in range(range_of_mas):
		column = []
		for row in range(range_of_mas):
			if mas[row][j] != 0:
				column.append(mas[row][j]) # сохраняем не нулевые
		
		while len(column) < range_of_mas:
			column.append(0) # добавим нули в конец

		for row in range(range_of_mas - 1):
			if column[row] == column[row + 1] and column[row] != 0: # тогда схлопываем
				column[row] *= 2 # хлоп!
				delta += column[row] # увеличим количество очков
				column.pop(row + 1) # удаляем соседа справа
				column.append(0) # добавляем 0 в конец ряда

		for row in range(range_of_mas):
			mas[row][j] = column[row]

	return mas, delta


# двигаем ячейки вниз и схлопываем
def move_down(mas, range_of_mas):
	delta = 0 # для подсчета очков
	for j in range(range_of_mas):
		column = []
		for row in range(range_of_mas):
			if mas[row][j] != 0:
				column.append(mas[row][j]) # сохраняем не нулевые
		
		while len(column) < range_of_mas:
			column.insert(0, 0) # добавим нули в начало

		for row in range(range_of_mas - 1, 0, -1):
			if column[row] == column[row - 1] and column[row] != 0: # тогда схлопываем
				column[row] *= 2 # хлоп!
				delta += column[row] # увеличим количество очков
				column.pop(row - 1) # удаляем соседа справа
				column.insert(0, 0) # добавляем 0 в начало ряда

		for row in range(range_of_mas):
			mas[row][j] = column[row]

	return mas, delta


# можем ли двигаться вообще, даже если нет свободных ячеек
def can_move(mas, range_of_mas):
	
	for row in range(range_of_mas - 1):
		for column in range(range_of_mas - 1):
			if mas[row][column] == mas[row][column + 1] or mas[row][column] == mas[row + 1][column]:
				return True

	return False

# end
