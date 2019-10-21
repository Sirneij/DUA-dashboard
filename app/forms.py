from flask_wtf          import FlaskForm, RecaptchaField
from flask_wtf.file     import FileField, FileRequired, FileAllowed
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired , Length
from . models    import User

class LoginForm(FlaskForm):
	email       = StringField  (u'Email'     , validators=[DataRequired(), Email()])
	password    = PasswordField(u'Password'        , validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')

class RegisterForm(FlaskForm):
	username    = StringField  (u'Username'  , validators=[DataRequired()])
	password    = PasswordField(u'Password'  , validators=[DataRequired()])
	email       = StringField  (u'Email'     , validators=[DataRequired(), Email()])
	firstName   = StringField  (u'FirstName'      , validators=[DataRequired()])
	lastName	= StringField  (u'LastName'      , validators=[DataRequired()])
	about 		= TextAreaField  (u'About')
	picture 	= FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one.')
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one.')

class UpdateAccountForm(FlaskForm):
    username    = StringField  (u'Username', validators=[DataRequired()])
    password    = PasswordField(u'Password', validators=[DataRequired()])
    email       = StringField  (u'Email', validators=[DataRequired(), Email()])
    firstName   = StringField  (u'FirstName', validators=[DataRequired()])
    lastName	= StringField  (u'LastName', validators=[DataRequired()])
    about		= TextAreaField  (u'About')
    picture 	= FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit 		= SubmitField('Update')
