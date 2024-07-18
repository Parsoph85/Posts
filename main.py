""" Для примера функционала будем использовать модули Юзер и Пост.
Данные модули имеют свои свойства, описанные в самих модулях.
Для хранения сущностей (объектов) будем юзать БД. В нашем случае легкую SQLite.
В ней будет 2 таблицы соответственно модулям.

Для обоснования процесса "Плодить сущности" модули выполняют специфические функции,
которые можно было написать в одном скрипте.

Кроме того, для уменьшения кода, отсутствует проверка на спецсимволы в запросах, использование несуществующих ИД.

Описание запросов: Идентификатор; Метод; Тело запроса

Добавление поста:
/posts ; POST ; {"body": "Text", "user": "Name"}

Просмотр определенного поста:
/posts?post_id=<ИД> ; GET ; нет

Просмотр всех постов:
/posts ; GET ; нет

Изменение поста:
/posts?post_id=<ИД> ; PUT ; {"body": "Text", "user": "Name"}

Удаление поста:
/posts?post_id=<ИД> ; DELETE ; нет

В отсутствии кода фронтенда, итогом работы будет вывод JSON.
"""

import json
import sqlite3

from flask import Flask, request, jsonify

from model.post import Posts

app = Flask(__name__)

conn = sqlite3.connect('posts.db')  # Создаем БД, если нет. И таблички, если нет
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (user_id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, passwd TEXT, email TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS posts 
                       (post_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, body TEXT, rating INT)''')
conn.commit()
cursor.close()


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Posts):
            return {'body': obj.body, 'author': obj.author}
        else:
            return super().default(obj)


@app.route('/posts', methods=['POST'])  # Создание поста
def create_post():
    post_json = request.get_json()  # Получаем данные из запроса
    json_data = json.dumps(post_json)  # Применяем кунг-фу для...
    post = json.loads(json_data)  # ... адекватного преобразования JSON в словарь
    body = post.get('body')  # Вытаскиваем из запроса значения
    user = post.get('user')
    posts = Posts().create(body=body, user=user)  # Хитрой магией отправляем значения на запись в БД
    return jsonify({'Status': posts})  # Информируем, что все хорошо



@app.route('/posts', methods=['GET'])  # Выводим нужный пост. Если нет id - ставим 0
def read_post():
    post_id = request.args.get('post_id', default=0, type=int)
    posts = Posts().read(post_id=post_id)
    return jsonify({'posts': posts})  # Экспорт в FE


@app.route('/posts', methods=['DELETE']) # Удаляем нужный пост
def del_post():
    post_id = request.args.get('post_id', type=int)
    posts = Posts().delete(post_id=post_id)
    return jsonify({'posts': posts})  # Экспорт в FE


@app.route('/posts', methods=['PUT'])  # Изменяем нужный пост
def change_post():
    post_id = request.args.get('post_id', type=int)
    post_json = request.get_json()  # Получаем данные из запроса
    json_data = json.dumps(post_json)  # Применяем кунг-фу для...
    post = json.loads(json_data)  # ... адекватного преобразования JSON в словарь
    body = post.get('body')  # Вытаскиваем из запроса значения
    user = post.get('user')
    posts = Posts().change(post_id=post_id,body=body,user=user)
    return jsonify({'posts': posts})  # Экспорт в FE

"""
Если реально кто-то читал этот код - нарисуйте в ответе змейку))) <XXXXXX(0)-<
Спасибо за терпение.
"""