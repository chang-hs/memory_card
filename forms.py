from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, DateField, BooleanField, SubmitField, PasswordField, DateTimeField
from wtforms.validators import InputRequired, Length, Optional

class CardRegisterForm(FlaskForm):
    lang = SelectField('Latin', choices=['Latin', 'French', 'Korean', 'Greek', 'English'])
    word = StringField('Word', validators=[InputRequired(),Length(max=20)])
    func = StringField('Funtion')
    meaning = StringField('Meaning', validators=[InputRequired()])
    memo = StringField('Memo')
    learnt = BooleanField('Learnt', default=False)
    difficult = IntegerField('Difficulty', default=0)
    submit = SubmitField('Submit')

class CardDisplayForm(FlaskForm):
    id = IntegerField('ID')
    word = StringField('Word', validators=[InputRequired(),Length(max=20)])
    func = StringField('Funtion')
    meaning = StringField('Meaning', validators=[InputRequired()])
    learnt = BooleanField('Learnt')
    difficulty = IntegerField('Difficulty')

class EditCardForm(FlaskForm):
    id = StringField('id')
    lang = SelectField('lang', choices=['Latin', 'French', 'Korean', 'English'])
    word = StringField('Word', validators=[InputRequired()])
    func = StringField('Func')
    meaning = StringField('Meaning', validators=[InputRequired()])
    memo = StringField('Memo')
    learnt = BooleanField('Learnt')
    difficulty = IntegerField('Difficulty')
    created_at = DateTimeField('Created')
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])
    submit = SubmitField('Login')