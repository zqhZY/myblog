from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from models import User
from __init__ import db
from wtforms import form, fields , validators
from werkzeug.security import generate_password_hash, check_password_hash
from config import REGIST_CODE

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
	login = fields.TextField(validators=[validators.required()])
	password = fields.PasswordField(validators=[validators.required()])

	def validate_login(self, field):
		user = self.get_user()
		if user is None:
			raise validators.ValidationError('Invalid user')
			
		# we're comparing the plaintext pw with the the hash from the d
		if not check_password_hash(user.password, self.password.data):		
		# to compare plain text passwords use
		# if user.password != self.password.data:
			raise validators.ValidationError('Invalid password')


	def get_user(self):
		return db.session.query(User).filter_by(login=self.login.data).first()

#admin registration form
class RegistrationForm(form.Form):
	login = fields.TextField(validators=[validators.required()])
	password = fields.PasswordField(validators=[validators.required()])
	registcode = fields.PasswordField(validators=[validators.required()])

	def validate_login(self, field):
		#check regist limit
		if self.registcode.data != REGIST_CODE:
			raise validators.ValidationError('Limited registcode')
		#check same user
		if db.session.query(User).filter_by(login=self.login.data).count() > 0:
			raise validators.ValidationError('Duplicate username')




#post search form
class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
