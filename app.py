# -*- coding: utf-8 -*-

import flask
import os
import random
import re

from flask import Flask, make_response, request, render_template, redirect, url_for, flash
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
#from flask.ext.mail import Mail
#from flask.ext.mail import Message
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask import render_template


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qdvcwjhjzx:KzsY5P8JzVuCY60RDmQ1@ec2-107-20-152-105.compute-1.amazonaws.com/qdvcwjhjzx'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
#mail = Mail(app)


class Bundle(db.Model):
	__tablename__ = 'bundle'
	id = db.Column(db.Integer, primary_key=True)
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	title = db.String(150)
	description = db.Column(db.Text)
	hash = db.Column(db.String(60))
	children = relationship('Media')

	def __init__(self, bundle_id, title, description):
		self.bundle_id = bundle_id
		self.title = title
		self.description = description
		self.hash = self._GenerateHash()

	def __repr__(self):
		return '<Bundle ID %r: %r>' % (self.id, self.title)

	def _GenerateHash(self):
		char_set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_';
		hash = '';
		for count in xrange(3):
			rand_num = random.randint(0, 63)
			hash += char_set[rand_num]

		# If the generated hash has already been used, try again.
		existing_hash = Bundle.query.filter_by(hash=hash).first()
		if existing_hash:
			return self._GenerateHash()

		return hash


class Media(db.Model):
	__tablename__ = 'media'
	id = db.Column(db.Integer, primary_key=True)
	bundle_id = db.Column(db.Integer, db.ForeignKey('bundle.id'))
	url = db.Column(db.String(120))
	thumburl = db.Column(db.String(120))
	type = db.Column(db.Integer)

	def __init__(self, bundle_id, url, thumburl, type):
		self.bundle_id = bundle_id
		self.url = url
		self.thumburl = thumburl
		self.type = type

	def __repr__(self):
		return '<Media ID %r: %r>' % (self.id, self.url)


class MediaType:
    IMAGE=1
    VIDEO=2


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(60), unique=False)
	active = db.Column(db.Boolean)

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password
		self.active = True

	def __repr__(self):
		return '<User %r>' % self.username


class UserLogin(UserMixin):
	def __init__(self, user):
		self.name = user.username
		self.id = user.id
		self.active = user.active

	def is_active(self):
		return self.active


class Anonymous(AnonymousUser):
	name = u"Anonymous"


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
	if user:
		return UserLogin(user)
	else:
		return None


login_manager.setup_app(app)

@app.route("/")
def home():
	if current_user and current_user.is_authenticated():
		return redirect(url_for("dashboard"))
	else:
		return redirect(url_for("index"))


@app.route("/addmedia", methods=["GET", "POST"])
@login_required
def add_media():
	if request.method == "POST" and ("bundleid" in request.form and
									 "url" in request.form and
									 "thumburl" in request.form):
		bundle_id = request.form["bundleid"]
		media_url = request.form["url"]
		media_type = get_media_type(media_url)
		if not media_type:
			flash('Could not determine media type.')
			return make_response(render_template('addmedia.html'), 400)
		elif media_type == MediaType.VIDEO:
			media_thumb_url = request.form["thumburl"]
		elif media_type == MediaType.IMAGE:
			media_thumb_url = request.form["thumburl"]

		new_media = Media(bundle_id, media_url, media_thumb_url, media_type)
		db.session.add(new_media)
		db.session.commit()
		flash("Media was successfully added!")
		return redirect(url_for("dashboard"))
	else:
		return render_template('addmedia.html')


def get_media_type(url):
	youtube_matcher = re.compile('^http:\/\/(?:www\.)?youtube\.com\/.*$')
	if youtube_matcher.match(url):
		return MediaType.VIDEO
	return None


@app.context_processor
def utility_processor():
	def get_user_bundles():
		return Bundle.query.filter_by(owner_id=current_user.id)
	return dict(get_user_bundles=get_user_bundles)


@app.route("/dashboard")
@login_required
def dashboard():
	return render_template("dashboard.html")


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST" and ("username" in request.form and
    								 "password" in request.form):
		username = request.form["username"]
		password = request.form["password"]
		user = User.query.filter_by(username=username).first()
		if user:
			remember = request.form.get("remember", "no") == "yes"

			if bcrypt.check_password_hash(user.password, password):
				if login_user(UserLogin(user), remember=remember):
					flash("Logged in!")
					return redirect(request.args.get("next") or url_for("dashboard"))
				else:
					flash("Sorry, but you could not log in.")
			else:
				flash("Incorrect password. Please try again.")
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
	if request.method == "POST" and ("username" in request.form and
									 "email" in request.form and
									 "password" in request.form):
		username = request.form["username"]
		email = request.form["email"]
		password = bcrypt.generate_password_hash(request.form["password"])

		user = User.query.filter_by(username=username).first()
		if user:
			flash(u"Username has already been taken!")
		else:
			user = User.query.filter_by(email=email).first()
			if user:
				flash(u"An account already exists for the specified email address.")
			else:
				user = User(username, email, password)
				db.session.add(user)
				db.session.commit()

				# Log the user in right after sign-up.
				if login_user(UserLogin(user)):
					return redirect(url_for("dashboard"))
				else:
					return redirect(url_for("index"))

#		flash("Yo you just gotcha self a lil email at %s!" % email)
#		msg = Message("Hello",
#			sender=("Bubblewrapp Admin", "noreply@bubblewrapp.com"),
#			recipients=[email])
#		msg.body = "testing"
#		msg.html = "<b>testing</b>"
#		mail.send(msg)
	return render_template("signup.html")


@app.route("/welcome")
def index():
	if current_user.is_authenticated():
		return redirect(url_for("dashboard"))
	else:
	    return render_template("index.html")


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
