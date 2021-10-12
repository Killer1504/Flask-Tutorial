from flask import Flask, render_template


posts = [
    {
        "author" : "Thanh Hung",
        "title" : "Blog post 1",
        "content": "First post Content",
        "date_posted" : "TuesDay, October 12"
    },
    {
        "author" : "Kim Duyen",
        "title" : "Blog post 2",
        "content": "Second post Content",
        "date_posted" : "TuesDay, October 12"
    }
]

def create_app():

    app = Flask(__name__)

    @app.route("/")
    @app.route("/home")
    def home():
        return render_template("home.html", posts=posts, title="Home")

    @app.route("/about")
    def about():
        return render_template("about.html", title="About")

    return app
