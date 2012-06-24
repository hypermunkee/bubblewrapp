# -*- coding: utf-8 -*-

import flask
import os

from flask import Flask, request, render_template, redirect, url_for, flash
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from flask.ext.mail import Mail
from flask.ext.mail import Message
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qdvcwjhjzx:KzsY5P8JzVuCY60RDmQ1@ec2-107-20-152-105.compute-1.amazonaws.com/qdvcwjhjzx'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mail = Mail(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60), unique=False)
    active = db.Column(db.Boolean)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email

		# To validate password later, use bcrypt.check_password_hash(dbpw, pw).
        self.password = password

        self.active = True

    def __repr__(self):
        return '<User %r>' % self.username


class UserLogin(UserMixin):
	def __init__(self, user):
		self.name = user.username
		self.id = user.id
		self.active = user.active

#    def __init__(self, name, id, active=True):
#        self.name = name
#        self.id = id
#        self.active = active

	def is_active(self):
		return self.active


class Anonymous(AnonymousUser):
    name = u"Anonymous"


#USERS = {
#    1: UserLogin(u"Notch", 1),
#    2: UserLogin(u"Steve", 2),
#    3: UserLogin(u"Creeper", 3, False),
#}

#USER_NAMES = dict((u.name, u) for u in USERS.itervalues())

SECRET_KEY = "yeah, not actually a secret"
DEBUG = True

app.config.from_object(__name__)

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

@login_manager.user_loader
def load_user(id):
	user = User.query.filter_by(id=id).first()
	return UserLogin(user)#USERS.get(int(id))


login_manager.setup_app(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/hello')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        user = User.query.filter_by(username=username).first()
        if user:#username in USER_NAMES:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(UserLogin(user), remember=remember):#USER_NAMES[username], remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))


@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("reauth.html")


@app.route("/secret")
@fresh_login_required
def secret():
    return render_template("secret.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
	if request.method == "POST" and "username" and "email" and "password" in request.form:
		username = request.form["username"]
		email = request.form["email"]
		password = bcrypt.generate_password_hash(request.form["password"])

		user = User(username, email, password)
		db.session.add(user)
		db.session.commit()

#		flash("Yo you just gotcha self a lil email at %s!" % email)
#		msg = Message("Hello",
#			sender=("Bubblewrapp Admin", "noreply@bubblewrapp.com"),
#			recipients=[email])
#		msg.body = "testing"
#		msg.html = "<b>testing</b>"
#		mail.send(msg)
	return render_template("signup.html")


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
