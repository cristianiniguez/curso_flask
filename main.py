from flask import request, make_response, redirect, render_template, session
from flask_login import login_required, current_user
import unittest

from app import create_app
from app.firestore_service import get_user, get_todos

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


@app.route('/hello', methods=['GET'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    user_id = current_user.id
    user = get_user(user_id)
    username = user.to_dict()['username']

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=user_id),
        'username': username
    }

    return render_template('hello.html', **context)
