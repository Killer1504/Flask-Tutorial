from flaskr import app
from flask import render_template, redirect, url_for, flash
from .forms import ResgistrationForm, LoginForm


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
    _form = ResgistrationForm()
    if _form.validate_on_submit():
        flash(f'Account created for {_form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    _form = LoginForm()
    if _form.validate_on_submit():
        if _form.email.data == "admin@blog.com" and _form.password.data == 'password':
            flash('You have been login!', "success")
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check username or password!', "danger")
    return render_template('login.html', title='Login', form=_form)