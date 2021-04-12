from flask import Flask, redirect, url_for, render_template, request, session
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import timedelta
from forms import LoginForm

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=60)
app.config.from_object(Config)
db = SQLAlchemy(app=app)


class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        # super(Users, db.Model).__init__()
        self.name = name
        self.email = email


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/view")
def view():
    return render_template("view.html", values=Users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.username.data
        session["user"] = user

        found_user = Users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = Users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash(f"Logged in {user} successfully", "info")
        return redirect(url_for("user"))

    if "user" in session:
        return redirect(url_for("user"))

    return render_template("login.html", form=form)


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = Users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email updated", "info")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)

    flash("Logged out successfully", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
