# dashboard/auth/login.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from auth.user import User
from common.config import conf

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == conf.get("email") and password == conf.get("password"):
            user = User(email)
            login_user(user)
            return redirect('/latest')
        else:
            flash('로그인 실패!', "warning")
    return render_template('login.html')
        
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template(url_for('auth.login'))