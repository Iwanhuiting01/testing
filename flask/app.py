from flask import Flask, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import BooleanField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ditisgeheim'

class InfoForm(FlaskForm):
    email = StringField('Wat is uw email?')
    newsletter = BooleanField('Wilt u de nieuwsbrief?')
    submit = SubmitField('Verzenden')

@app.route('/', methods=('GET', 'POST'))
def index():
    print(request.args)
    print(request.form)
    form = InfoForm()
    if form.validate_on_submit():
        email = form.email.data
        return render_template('index.html' , email=email)


    return render_template('index.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = InfoForm()
    if form.validate_on_submit():
        email = form.email.data
        return render_template('login.html')

    return render_template('login.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = InfoForm()
    if form.validate_on_submit():
        email = form.email.data
        return render_template('register.html')

    return render_template('register.html')

@app.route('/movie', methods=('GET', 'POST'))
def movie():
    form = InfoForm()
    if form.validate_on_submit():
        email = form.email.data
        return render_template('movie.html')

    return render_template('movie.html')

@app.route('/movie/create', methods=('GET', 'POST'))
def create_movie():
    form = InfoForm()
    if form.validate_on_submit():
        email = form.email.data
        return render_template('create_movie.html')

    return render_template('create_movie.html')

if __name__ == '__main__':
    app.run(debug=True)


app = Flask(__name__, static_url_path='/static')
