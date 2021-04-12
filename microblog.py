# from flask import redirect, url_for, session
from app import app, db


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
