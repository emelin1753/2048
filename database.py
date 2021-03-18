import sqlite3

db= sqlite3.connect("2048.sqlite")
cursor = db.cursor()
cursor.execute("CREATE TABLE if not exists RECORDS (name TEXT, score INTEGER)")


# извлекаем из БД 3 лучших результата
def get_best_score():
	cursor.execute("""SELECT name gamer, max(score) score from RECORDS
		GROUP by name ORDER by score DESC limit 3""")
	# поле name и max(score) представим в виде gamer и score = name gamer, max(score) score
	# группируем по name, чтобы не было повторов одного и того же игрока = GROUP by name
	# упорядочиваем по score по убыванию = ORDER by score DESC
	# берем 3 самых первых = limit 3
	return cursor.fetchall()


# добавляем в БД текущий результат
def insert_result(name, score):
	cursor.execute("""INSERT into RECORDS values (?, ?)""", (name, score))
	db.commit()

