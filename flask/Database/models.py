from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Models
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.Text, unique=True)
    user_name = db.Column(db.Text)
    password = db.Column(db.Text)
    comments = db.relationship('Comment', back_populates="user")

    def __init__(self, email, user_name, password):
        self.email = email
        self.user_name = user_name
        self.password = password


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    release_year = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    youtube_link = db.Column(db.Text)
    director = db.relationship('Director', back_populates="movies")
    comments = db.relationship('Comment', back_populates="movie")

    def __init__(self, title, director_id, release_year, user_id, description, youtube_link):
        self.title = title
        self.director_id = director_id
        self.release_year = release_year
        self.user_id = user_id
        self.description = description
        self.youtube_link = youtube_link


class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    movies = db.relationship('Movie', back_populates="director")

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie = db.relationship('Movie', back_populates="comments")
    user = db.relationship('User', back_populates="comments")

    def __init__(self, body, movie_id, user_id):
        self.body = body
        self.movie_id = movie_id
        self.user_id = user_id
