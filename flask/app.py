import os
import sqlite3

# Models
from testing.flask.Database.models import *
# Forms
from testing.flask.Database.forms import *

from flask import Flask, render_template, g, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

basedir = os.path.abspath(os.path.join(__file__, "../.."))

print(basedir)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ditisgeheim'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'filmfan.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# Forms

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_update_query(table_name, where_vals, update_vals):
  query = table_name.update()
  for k, v in where_vals.iteritems():
    query = query.where(getattr(table_name.c, k) == v)
  return query.values(**update_vals)

def get_db():
    DATABASE = '../filmfan.db'
    db2 = getattr(g, '_database', None)
    if db2 is None:
        db2 = g._database = sqlite3.connect(DATABASE)
    return db2


@app.route('/', methods=('GET', 'POST'))
def index():
    movies = Movie.query.all()
    form = InfoForm()
    if form.validate_on_submit():
        email = form.email.data
        return render_template('index.html', email=email)

    return render_template('index.html', form=form, movies=movies)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    print('hello')
    if form.validate_on_submit():
        print('hello')
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        print(user)
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.user_name.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            return redirect(url_for('register'))

        user = User(email, username, generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/movie/<id>', methods=('GET', 'POST'))
def movie(id):
    movie = Movie.query.get(id)
    comments = movie.comments
    comments.reverse()
    form = PostComment()

    if form.validate_on_submit():
        body = form.body.data
        user_id = current_user.id
        movie_id = id

        comment = Comment(body, movie_id, user_id)
        db.session.add(comment)
        db.session.commit()

        flash('Comment gepost')
        return redirect(url_for('movie', id=movie.id))

    return render_template('movie.html', movie=movie, form=form, comments=comments)

@app.route('/movie/create', methods=('GET', 'POST'))
@login_required
def create_movie():
    directors = Director.query.all()
    directors_list = [(i.id, i.first_name + ' ' + i.last_name) for i in directors]

    form = CreateMovieForm()
    form.director.choices = directors_list

    if form.validate_on_submit():
        title = form.title.data
        director = form.director.data
        release_year = form.release_year.data
        user_id = current_user.id
        description = form.description.data
        youtube_link = form.youtube_link.data

        movie = Movie(title, director, release_year, user_id, description, youtube_link)
        db.session.add(movie)
        db.session.commit()
        movie_id = movie.id
        flash('Film aangemaakt')
        return redirect(url_for('movie', id=movie_id))

    return render_template('create_movie.html', form=form)

@app.route('/movies/edit')
@login_required
def edit_movies_panel():
    movies = Movie.query.all()
    return render_template('edit_movie_panel.html', movies=movies)

@app.route('/delete/movie/<id>')
@login_required
def delete_movie(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('edit_movies_panel'))

@app.route('/edit/movie/<id>', methods=('GET', 'POST'))
@login_required
def edit_movie(id):
    movie = Movie.query.get(id)
    form = EditMovieForm(director=movie.director_id)

    directors = Director.query.all()
    movie.director = Director.query.get(movie.director_id)
    directors_list = [(i.id, i.first_name + ' ' + i.last_name) for i in directors]

    form.director.choices = directors_list

    if form.validate_on_submit():
        title = form.title.data
        director = form.director.data
        release_year = form.release_year.data
        user_id = current_user.id
        description = form.description.data
        youtube_link = form.youtube_link.data

        movie.title = title
        movie.director_id = director
        movie.release_year = release_year
        movie.user_id = user_id
        movie.description = description
        movie.youtube_link = youtube_link

        db.session.add(movie)
        db.session.commit()
        movie_id = movie.id
        flash('Film aangepast')
        return redirect(url_for('movie', id=movie_id))
    else:
        form.description.data = movie.description

    return render_template('edit_movie.html', movie=movie, form=form, directors=directors)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


app = Flask(__name__, static_url_path='/static')
