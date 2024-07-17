""" Для примера функционала будем использовать модули Юзер и Пост.
Данные модули имеют свои свойства, описанные в самих модулях.
Для хранения сущностей (объектов) будем юзать БД. В нашем случае легкую SQLite.
В ней будет 2 таблицы соответственно модулям.
Для обоснования процесса "Плодить сущности" модули выполняют специфические функции,
которые можно было написать в одном скрипте.

Описание запросов: Идентификатор; Метод; Тело запроса

Добавление поста:
/posts ; POST ; {"body": "Text", "user": "Name"}

Просмотр определенного поста:
/posts/<post id> ; GET ; нет

Просмотр всех постов:
/posts ; GET ; нет

Изменение поста:
/posts/<post id> ; PUT ; {"body": "Text", "user": "Name"}

Удаление поста:
/posts/<post id> ; DELETE ; нет

В отсутствии кода фронтенда, итогом работы будет вывод JSON
"""

import json
import sqlite3

from flask import Flask, request, jsonify

from model.post import Posts

app = Flask(__name__)

conn = sqlite3.connect('posts.db')  # Создаем БД, если нет. И таблички, если нет
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (id_user INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, passwd TEXT, email TEXT)''')
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
    posts = Posts().Create(body=body, user=user)  # Хитрой магией отправляем значения на запись в БД
    return jsonify({'Status': posts})  # Информируем, что все хорошо


@app.route('/posts', methods=['GET'])  # Выводим все посты
def read_all_post():
    posts = Posts().Read()
    print(posts)  #{'body': 'Text', 'user': 'Name'},{'body': 'Text', 'user': 'Name'}
    return jsonify({'posts': posts})  # Выводим все посты


@app.route('/posts/<post_id>', methods=['GET'])  # Выводим нужный посты
def read_post(post_id):
    posts = Posts.post(post_id=post_id, action='read')
    print(posts)


@app.route('/posts', methods=['DELETE'])
def delete_post():
    """ Пример запроса {"id": ""}
    id - номер удаляемого поста"""

    del_json = request.get_json()  # Получаем данные из запроса
    json_data = json.dumps(del_json)  # Применяем кунг-фу для...
    del_dict = json.loads(json_data)  # ... адекватного преобразования JSON в словарь
    print(del_dict)
    del_elem = "'id': '" + del_dict['id'] + "'"
    print(del_elem)

    #del posts[del_elem]
    return jsonify({'status': 'success'})  # Информируем, что все хорошо
    return jsonify({'posts': posts})
