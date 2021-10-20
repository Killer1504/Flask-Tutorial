import flask_login
from flaskr import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from .forms import ResgistrationForm, LoginForm, UpdateAccountForm, PostForm
from .models import User, Post
import secrets
import os
from PIL import Image

from flask_login import login_user, current_user, logout_user, login_required




@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
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
        hashed_pw = bcrypt.generate_password_hash(
            _form.password.data).decode('utf-8')
        user = User(username=_form.username.data,
                    email=_form.email.data, password=hashed_pw)
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # resize image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    _form = UpdateAccountForm()
    if _form.validate_on_submit():
        if _form.picture.data:
            picture_file = save_picture(_form.picture.data)
            current_user.image_file = picture_file
            pass
        current_user.username = _form.username.data
        current_user.email = _form.email.data
        db.session.commit()
        flash('Your accout has been update!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        _form.username.data = current_user.username
        _form.email.data = current_user.email
    else:
        flash('Your accout cannot be update!', 'danger')
        return redirect(url_for('account'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=_form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    _form = PostForm()
    if _form.validate_on_submit():
        post = Post(title=_form.title.data, content=_form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post have been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=_form)
