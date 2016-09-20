from flask import render_template,redirect, request, url_for, flash
from flask.ext.login import login_user,login_required,logout_user,current_user

from . import main
from .forms import RegistrationForm,LoginForm
from .. import db
from ..models import User

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=None,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('creat user ok.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login',methods = ['GET','POST'])
def login():
    #db.create_all()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout ok')
    return redirect(url_for('main.index'))

@main.route('/playSnake')
def playSnake():
    return render_template('play/snake.html')