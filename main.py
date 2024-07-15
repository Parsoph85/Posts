import json

from flask import Flask, request, jsonify
from model.post import Posts

posts = []

app = Flask(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Posts):
            return {'body': obj.body, 'author': obj.author}
        else:
            return super().default(obj)

@app.route('/post', methods=['POST'])
def create_post():
    ''' {"body": "", "author": "TestName"} '''
    post_json = request.get_json()
    post = Posts(post_json["body"], post_json["author"])
    posts.append(post)
    print(posts)
    return jsonify({'status': 'success'})

@app.route('/post', methods=['GET'])
def read_post():
    return jsonify({'posts': posts})
