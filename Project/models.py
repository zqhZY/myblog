#encoding= utf-8

from hashlib import md5
#from datetime import datetime
from __init__ import app , db
from flask.ext.login import UserMixin
import sys
'''
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy
'''
#friend followed :many to many

ROLE_ADMIN = 1
ROLE_USER = 2


# 用户
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	login = db.Column(db.String(80), unique=True)
	nickname = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(64), unique=True)
	email = db.Column(db.String(120), unique=True)
	role = db.Column(db.SmallInteger, default=ROLE_ADMIN)
	entry = db.relationship('Post', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(250))
	last_seen = db.Column(db.DateTime)
		       # Flask-Login integration
	def is_authenticated(self):
		return True
		
	def is_active(self):
		return True

	def is_anonymous(self):
		return False												       
	
	def get_id(self):
		return self.id
		
	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % self.nickname
		
	


# 分类
		
class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	
	def __repr__(self):
		return '<Category %r>' % self.name

	def __unicode__(self):
		return self.name

# 标签
class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	
	def __repr__(self):
		return '<Tag %r>' % self.name

tag_entry = db.Table('tags',
		db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
		db.Column('entry_id', db.Integer, db.ForeignKey('post.id'))
		)

class Post(db.Model):
	#__searchable__ = ['body']
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	body = db.Column(db.Text)
	fragment = db.Column(db.Text)
	status = db.Column(db.Integer, default=1) 
	create_time = db.Column(db.DateTime, index=True)
	modified_time = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'), lazy='select')
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	tag = db.relationship('Tag', secondary=tag_entry, backref=db.backref('posts', lazy='dynamic'))
	view_count = db.Column(db.Integer, default=0)
	
	def __repr__(self):
		return '<Entry %r>' % self.title
		
	def __unicode__(self):
		return self.title
  

#whooshalchemy.whoosh_index(app, Post)
