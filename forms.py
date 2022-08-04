from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), 
                                     EqualTo('password')])
    age = StringField('Age',
                        validators=[DataRequired()])
    zip_c = StringField('Zip Code',
                        validators=[DataRequired()])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class MealForm(FlaskForm):
    period = StringField('Period')
    diet = StringField('Diet')
    calories= StringField('Calories')
    exclude= StringField('exclude')
    #submit= StringField('Generate')
