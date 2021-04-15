from flask import redirect, url_for, render_template, flash, request
from app import app
from app.models import User
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route("/user", methods=["POST", "GET"])
def user():
    return render_template("user.html", email=None)


@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html")


@app.route("/view")
# @login_required
def view():
    return render_template("view.html", values=User.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid name or password")
            redirect(url_for("login"))

        flash(f"Logged in {user} successfully", "info")
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user')        
        return redirect(url_for("user"))

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))
