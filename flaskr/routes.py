import flask_login
from flaskr import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from .forms import ResgistrationForm, LoginForm
from .models import User, Post

from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        "author": "Thanh Hung",
        "title": "Blog post 1",
        "content": "First post Content",
        "date_posted": "TuesDay, October 12"
    },
    {
        "author": "Kim Duyen",
        "title": "Blog post 2",
        "content": "Second post Content",
        "date_posted": "TuesDay, October 12"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts, title="Home")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_active:
        return redirect(url_for('home'))
    _form = ResgistrationForm()
    if _form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(_form.password.data).decode('utf-8')
        user = User(username=_form.username.data, email=_form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are able log in now!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_active:
        return redirect(url_for('home'))
    _form = LoginForm()
    if _form.validate_on_submit():
        user = User.query.filter_by(email=_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, _form.password.data):
            flash(f'Login Successfult. Welcom {user.username}!', "success")
            login_user(user, remember=_form.remember.data)
            # redirect to next page if user get webpage another
            # Example: user not login, but user want to get {url}/account
            # After login, web to redirect {url}/account instead {url}/home
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check email or password!', "danger")
    return render_template('login.html', title='Login', form=_form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')