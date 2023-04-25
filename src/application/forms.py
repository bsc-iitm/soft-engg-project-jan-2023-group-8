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

class TicketForm(FlaskForm):
    subject = StringField(label='Subject', validators=[DataRequired()])
    category=StringField(label='Category',validators=[DataRequired()])
    submit = SubmitField(label='Add Ticket')

class EditTicket(FlaskForm):
    new_subject = StringField(label='Enter New Subject', validators=[DataRequired()])
    new_category = StringField(label='Change Category?', validators=[DataRequired()])
    edit = SubmitField(label='Edit Ticket')

class MessageForm(FlaskForm):
    content = StringField(label='Enter Reply Message', validators=[DataRequired()])
    submit = SubmitField(label='Add Message')

class EditMessage(FlaskForm):
    new_content = StringField(label='Enter New Question', validators=[DataRequired()])
    edit = SubmitField(label='Edit')


class DeleteForm(FlaskForm):
    delete = SubmitField(label='Delete')
