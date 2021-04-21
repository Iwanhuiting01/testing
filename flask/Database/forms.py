from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, InputRequired

class InfoForm(FlaskForm):
    email = StringField('Wat is uw email?')
    newsletter = BooleanField('Wilt u de nieuwsbrief?')
    submit = SubmitField('Verzenden')


class RegisterForm(FlaskForm):
    email = StringField('E-mail:', validators=[DataRequired()])
    user_name = StringField('Gebruikers naam:', validators=[DataRequired()])
    password = PasswordField('Wachtwoord:', validators=[DataRequired()])
    submit = SubmitField('Verzenden')


class LoginForm(FlaskForm):
    email = StringField('E-Mail:', validators=[DataRequired()])
    password = PasswordField('Wachtwoord:', validators=[DataRequired()])
    submit = SubmitField('Verzenden')


class CreateMovieForm(FlaskForm):
    title = StringField('Titel:', validators=[DataRequired()],  render_kw={"placeholder": "Naam"})
    director = SelectField('Regisseur', coerce=str, validators=[InputRequired()])
    release_year = StringField('Jaar:', validators=[DataRequired()],  render_kw={"placeholder": "Jaar"})
    description = TextAreaField('Beschrijving:', validators=[DataRequired()],  render_kw={"placeholder": "Beschrijving"})
    youtube_link = StringField('Link:', validators=[DataRequired()],  render_kw={"placeholder": "Youtube id (na watch?v=)"})

class EditMovieForm(FlaskForm):
    title = StringField('Titel:', validators=[DataRequired()],  render_kw={"placeholder": "Naam"})
    director = SelectField('Regisseur', coerce=str, validators=[InputRequired()])
    release_year = StringField('Jaar:', validators=[DataRequired()],  render_kw={"placeholder": "Jaar"})
    description = TextAreaField('Beschrijving:', validators=[DataRequired()],  render_kw={"placeholder": "Beschrijving"})
    youtube_link = StringField('Link:', validators=[DataRequired()],  render_kw={"placeholder": "Youtube id (na watch?v=)"})

class PostComment(FlaskForm):
    body = TextAreaField('Beschrijving:', validators=[DataRequired()],  render_kw={"placeholder": "Beschrijving"})
    submit = SubmitField('POST COMMENT')