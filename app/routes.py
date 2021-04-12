from flask import redirect, url_for, render_template, session, flash
from app import app, db
from app.models import User
from app.forms import LoginForm


@app.route("/user", methods=["POST", "GET"])
def user():
    return render_template("user.html", email=None)


@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html")


@app.route("/view")
def view():
    return render_template("view.html", values=User.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.username.data
        session["user"] = user

        found_user = User.query.filter_by(username=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = User()
            usr.username = user

            db.session.add(usr)
            db.session.commit()

        flash(f"Logged in {user} successfully", "info")
        return redirect(url_for("user"))

    if "user" in session:
        return redirect(url_for("user"))

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)

    flash("Logged out successfully", "info")
    return redirect(url_for("login"))
