from flask import request, make_response, redirect, render_template, session, flash
from flask.helpers import url_for
from flask_login import login_required, current_user
import unittest

from app import create_app
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm
from app.firestore_service import get_user, get_todos, create_todo, delete_todo, update_todo

app = create_app()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    user_id = current_user.id
    user = get_user(user_id)
    username = user.to_dict()['username']

    todo_form = TodoForm()
    delete_todo_form = DeleteTodoForm()
    update_todo_form = UpdateTodoForm()

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=user_id),
        'username': username,
        'todo_form': todo_form,
        'delete_todo_form': delete_todo_form,
        'update_todo_form': update_todo_form,
    }

    if todo_form.validate_on_submit():
        create_todo(user_id=user_id, description=todo_form.description.data)
        flash('Tu tarea se creo con éxito')
        return redirect(url_for('hello'))

    return render_template('hello.html', **context)


@app.route('/todo/delete/<id>', methods=['POST'])
def delete(id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=id)
    return redirect(url_for('hello'))


@app.route('/todo/update/<id>/<int:done>', methods=['POST'])
def update(id, done):
    user_id = current_user.id
    update_todo(user_id=user_id, todo_id=id, done=done)
    return redirect(url_for('hello'))
