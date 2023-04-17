from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired,EqualTo,Email

class RegistrationForm(FlaskForm):
    username = StringField('username', validators =[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    role = SelectField("Role", choices=[('1', 'Student'), ('2', 'Support Staff'),('3', 'Support Admin')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')