""" Имеется в виду, что каждая модель является классом. Модели нужны для создания
объектов по их свойствам.
Для поста это: ИД, ИД пользователя, Текст, Рейтинг.
Поля добавим все, но используем только ИД, ИД пользователя и Текст"""
import sqlite3

from model.user import User # Импортируем модель юзеров


class Posts:
    def __init__(self, *a):
        pass

    def Create(self, body: str, user: str): # Создание новой записи. В качестве аргументов у нас пост и имя юзера
        self.user = user
        self.body = body
        user_id = User().Work(user=user) # Вытягиваем ИД при помощи модуля Юзеров
        conn = sqlite3.connect('posts.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (user_id, body) VALUES (?, ?)", (user_id, body)) # Скармливаем в БД
        conn.commit()
        conn.close()
        return ("Success")

    def Read(self, all=0):
        self.all = all
        if all == 0:
            conn = sqlite3.connect('posts.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM posts")
            lдописать кусок догики на то, чтобы шерстить бд построчно, менять ид юзера на имя,
            преобразовывать в JSON, слеплять в один список и отправлять обратно

