import os
import sqlite3

from flask import Flask, render_template, g, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.join(__file__, "../.."))
print(basedir)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ditisgeheim'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'filmfan.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Forms

class InfoForm(FlaskForm):
    email = StringField('Wat is uw email?')
    newsletter = BooleanField('Wilt u de nieuwsbrief?')
    submit = SubmitField('Verzenden')


class RegisterForm(FlaskForm):
    email = StringField('E-mail:', validators=[DataRequired()])
    user_name = StringField('Gebruikers naam:', validators=[DataRequired()])
    password = PasswordField('Wachtwoord:', validators=[DataRequired()])
    submit = SubmitField('Verzenden')

# Models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.Text, unique=True)
    user_name = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self, email, user_name, password):
        self.email = email
        self.user_name = user_name
        self.password = password

    # def __repr__(self):
    #     return f"Cursist {self.naam} is {self.leeftijd} jaar oud"


def get_db():
    DATABASE = '../filmfan.db'
    db2 = getattr(g, '_database', None)
    if db2 is None:
        db2 = g._database = sqlite3.connect(DATABASE)
    return db2

@app.route('/', methods=('GET', 'POST'))
def index():
    db2 = get_db().cursor()
    movies = db2.execute('select * from movies').fetchall()
    form = InfoForm()
    if form.validate_on_submit():
        email = form.email.data
        return render_template('index.html', email=email)

    return render_template('index.html', form=form, movies=movies)


@app.route('/login', methods=('GET', 'POST'))
def login():

    return render_template('login.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.user_name.data
        password = form.password.data

        user = User(email, username, password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/movie/<id>', methods=('GET', 'POST'))
def movie(id):
    db2 = get_db().cursor()
    movie = db2.execute('select * from movies WHERE id = ?;', (id)).fetchone()

    director = db2.execute('select * from directors WHERE id = ?;', (movie[2])).fetchone()

    return render_template('movie.html', movie=movie, director=director)

@app.route('/movie/create', methods=('GET', 'POST'))
def create_movie():

    return render_template('create_movie.html')

if __name__ == '__main__':
    app.run(debug=True)


app = Flask(__name__, static_url_path='/static')
