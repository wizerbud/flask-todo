from uuid import uuid4
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)


class Todo:
    def __init__(self, text):
        self.uuid = uuid4()
        self.text = text

    @property
    def id(self):
        return str(self.uuid)

    def __repr__(self):
        return f'<Todo: {self.text}>'

class Todos:
    data = []

    @staticmethod
    def add(todo: Todo):
        Todos.data.append(todo)

    @staticmethod
    def remove(todo: Todo):
        Todos.data = [item for item in Todos.data if todo.id != item.id]

    @staticmethod
    def find(id):
        return [todo for todo in Todos.data if todo.id == id]


    def reset(self):
        self.todos = []


@app.route('/') 
def home():
    return render_template('index.html', todos=Todos.data)


@app.route('/create', methods=('POST',)) 
def create_todo():
    text = request.form.get('text')
    if not text:
        text = 'Unknown'
    Todos.add(Todo(text))
    return redirect(url_for('home'))


@app.route('/delete/<id>', methods=('POST',)) 
def delete_todo(id):
    id = request.form.get('id')
    result = Todos.find(id)
    if result:
        Todos.remove(result[0])
    return redirect(url_for('home'))

if __name__ == '__mane__':
    app.run()
