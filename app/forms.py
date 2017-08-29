from flask_wtf import Form
from wtforms import  StringField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired

# Login Form
class LoginForm(Form):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

# Regsiter Form
class RegisterForm(Form):
    firstname = StringField('firstname', [validators.DataRequired()])
    lastname = StringField('lastname', [validators.DataRequired()])
    email = StringField('email', [validators.DataRequired()])
    username = StringField('username', [validators.Length(min=4)])
    password = PasswordField('password', [validators.Length(min=6, max=25), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('confirm')

# Ticker Form
class TickerForm(Form):
    ticker = StringField('ticker', [validators.DataRequired()])
    