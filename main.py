from flask import Flask, request, jsohify
from model.post import Posts

posts = []

app = Flask(_ _name_ _)

@app.route(’/posts’, methods=[’POST’])
def create_post():
    ''' {"body": "", "author": "TestName"} '''
    post_json = request.get.json()
    post = Posts(post_json['body'], post_json['author'])
    posts.append(post)
    return jsohify({'status': 'success'})

@app.route(’/posts’, methods=[’GET’])
def read_post():
    return jsohify({'posts': posts})
