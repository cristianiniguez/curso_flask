from flask import render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user

from . import auth
from app.forms import LoginForm
from app.models import UserData, UserModel
from app.firestore_service import get_user_by_name


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form,
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user_by_name(username)
        if (user_doc is not None and user_doc.to_dict() is not None):
            password_from_db = user_doc.to_dict()['password']
            if (password == password_from_db):
                user_data = UserData(user_doc.id, username, password)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo')
                redirect(url_for('hello'))
            else:
                flash('Información incorrecta')
        else:
            flash('Usuario no encontrado')

        return redirect(url_for('index'))

    return render_template('login.html', **context)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')
    return redirect(url_for('auth.login'))
