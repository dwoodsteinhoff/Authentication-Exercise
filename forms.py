from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email

class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Please enter a valid Username")])

    password = PasswordField("Password", validators=[InputRequired(message="Please enter a valid Password")])

    email = StringField("Email", validators=[InputRequired(),Email(message="Please enter a valid Email")])

    first_name = StringField("First Name", validators=[InputRequired()])
    
    last_name = StringField("Last Name", validators=[InputRequired()])


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(message="Please enter a title")])
    content = StringField("Feedback", validators=[InputRequired(message="Please enter feedback")])