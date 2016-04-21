 #encoding=utf-8

from flask import Flask, url_for, redirect, render_template, request
from __init__ import app , db  
from models import (User , Post , Category , Tag)
from forms import LoginForm , RegistrationForm
from flask.ext.admin import Admin , BaseView  ,expose#my admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from werkzeug.security import generate_password_hash, check_password_hash
import os.path as op
from flask_admin.contrib import sqla
import flask_admin as admin
import flask_login as login
from flask_admin import helpers, expose
#init flask-login
def init_login():
	login_manager = login.LoginManager()
	login_manager.init_app(app)
	
	@login_manager.user_loader
	def load_user(user_id):
		return db.session.query(User).get(user_id)

class MyModelView(sqla.ModelView):
	def is_accessible(self):
		return login.current_user.is_authenticated()

# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):
	
	@expose('/')
	def index(self):
		if not login.current_user.is_authenticated():
			return redirect(url_for('.login_view'))
		return super(MyAdminIndexView, self).index()

	@expose('/login/', methods=('GET', 'POST'))
	def login_view(self):
	# handle user login
		form = LoginForm(request.form)
		if helpers.validate_form_on_submit(form):
			user = form.get_user()
			login.login_user(user)

		if login.current_user.is_authenticated():
			return redirect(url_for('.index'))
		
		link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
		self._template_args['form'] = form
		self._template_args['link'] = link
		return super(MyAdminIndexView, self).index()

	@expose('/register/', methods=('GET', 'POST'))
	def register_view(self):
		form = RegistrationForm(request.form)
		if helpers.validate_form_on_submit(form):
			user = User()
			form.populate_obj(user)
			# we hash the users password to avoid saving it as plaintext in the db,
			# remove to use plain text:
			user.password = generate_password_hash(form.password.data)
	        
			db.session.add(user)
			db.session.commit()
			login.login_user(user)

			return redirect(url_for('.index'))
		link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
		self._template_args['form'] = form
		self._template_args['link'] = link
		return super(MyAdminIndexView, self).index()

	@expose('/logout/')
	def logout_view(self):
		login.logout_user()
		return redirect(url_for('.index'))


#flask view
	
'''
class myview(BaseView):

	def is_accessible(self):
		return True
	@expose('/')
	def index(self):
		return self.render('admin.html')
'''


init_login()

admin = admin.Admin(app, index_view=MyAdminIndexView(),
		base_template='my_master.html')
	  

admin.add_view(MyModelView(User , db.session))
admin.add_view(MyModelView(Post , db.session))
admin.add_view(MyModelView(Category , db.session))
admin.add_view(MyModelView(Tag , db.session))

path = op.join(op.dirname(__file__) , 'static')
#admin.add_view(FileAdmin(path , '/static/' , name = 'static files'))
#admin = Admin(app)


