""" Имеется в виду, что каждая модель является классом. Модели нужны для создания
объектов по их свойствам.
Для поста это: ИД, ИД пользователя, Текст, Рейтинг.
Поля добавим все, но используем только ИД, ИД пользователя и Текст"""
import sqlite3

from model.user import User  # Импортируем модель юзеров


class Posts:
    def __init__(self, *a):
        pass

    def сreate(self, body: str, user: str):  # Создание новой записи. В качестве аргументов у нас пост и имя юзера
        self.user = user
        self.body = body
        user_id = User().work(user=user)  # Вытягиваем ИД при помощи модуля Юзеров
        conn = sqlite3.connect('posts.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (user_id, body) VALUES (?, ?)", (user_id, body))  # Скармливаем в БД
        conn.commit()
        conn.close()
        return ("Success")  # Отдаем результат для передачи в JSON

    def read(self, post_id=0):  # Чтение записи. В качестве аргументов у нас ИД поста
        self.post_id = int(post_id)
        post = []
        if post_id == 0:  # Если ИД не передавалось...
            conn = sqlite3.connect('posts.db')
            cursor = conn.cursor()
            all = cursor.execute(f"SELECT * FROM posts")  # ... читаем все посты...
            for line in all:
                user_id = line[1]  # ... получаем ИД юзера...
                user = User().get_user(user_id=user_id)  # ... из него - Имя юзера...
                dict = {'body': line[2], 'user': user}  # ... их пишем в словарь...
                post.append(dict)  # ... собираем словарь в список.
        else:
            conn = sqlite3.connect('posts.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM posts WHERE post_id = '{post_id}'")  # Если был номер поста...
            line = cursor.fetchone()
            user_id = line[1]
            user = User().get_user(user_id=user_id)  # ... делаем все то же, но для одной строки.
            dict = {'body': line[2], 'user': user}
            post.append(dict)
        conn.commit()
        conn.close()
        return (post)  # Отдаем результат в виде словаря для передачи в JSON

    def delete(self, post_id):  # Удаление поста. Аргумент - номер поста
        self.post_id = int(post_id)
        conn = sqlite3.connect('posts.db')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM posts WHERE post_id='{post_id}'")  # Просто удаляем строку.
        conn.commit()
        conn.close()
        return ("Success delete")  # Отдаем результат для передачи в JSON

    def change(self, post_id: int, body: str,
               user: str):  # Изменение записи. В качестве аргументов у нас номер поста, пост и имя юзера
        self.post_id = post_id
        self.user = user
        self.body = body
        user_id = User().work(user=user)  # Вытягиваем ИД при помощи модуля Юзеров
        conn = sqlite3.connect('posts.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE posts SET body = '{body}', user_id = '{user_id}' WHERE post_id = '{post_id}'")
        conn.commit()
        conn.close()
        return ("Success")  # Отдаем результат для передачи в JSON
