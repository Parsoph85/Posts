""" Имеется в виду, что каждая модель является классом. Модели нужны для создания
объектов по их свойствам.
Для юзера это ИД, имя, пароль, мыло. Поля добавим все, но используем только ИД, имя"""
import sqlite3


class User:
    def __init__(self, *a):
        pass

    def work(self, user: str):  # Получаем имя
        self.user = user
        conn = sqlite3.connect('posts.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE user = '{user}'")  # Проверяем есть ли имя в БД
        result = cursor.fetchone()
        if result:
            user_id = result[0]  # Если есть - выдаем его ИД
        else:
            cursor.execute(f"INSERT INTO users (user) VALUES ('{user}')")  # Если нет - пишем имя в БД
            cursor.execute(f"SELECT * FROM users WHERE user = '{user}'")  # и выдаем его ИД
            result = cursor.fetchone()
            user_id = result[0]
        conn.commit()  # Фиксируем результат
        conn.close()  # Закрываем БД
        return user_id  # Передаем ИД обратно

    def get_user(self, user_id):
        self.user_id = user_id
        conn = sqlite3.connect('posts.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")  # Получаем юзера по ИД
        result = cursor.fetchone()
        user = result[1]
        conn.commit()  # Фиксируем результат
        conn.close()  # Закрываем БД
        return user  # Передаем Имя обратно
