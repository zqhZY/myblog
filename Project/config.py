import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

REGIST_CODE = ''#os.environ.get('MYSQL_USER')


from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)


# -- Flask - SQLALCHEMY --
'''
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_USER = 'root'#os.environ.get('MYSQL_USER')
MYSQL_PASS = 'zqh'#os.environ.get('MYSQL_PASSWORD')
MYSQL_DB = 'blog3'#os.environ.get('MYSQL_DATABASE')
'''
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

SQLALCHEMY_POOL_RECYCLE = 10

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WHOOSH_BASE = os.path.join(basedir, 'search.db')

#SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' \
#						  % (MYSQL_USER, MYSQL_PASS,
#								  MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

'''
# email server
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'zqh563078785@163.com'#os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = '19921017100'#os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = ['zqh563078785@163.com']
'''
# pagination
POSTS_PER_PAGE = 5
#POSTS_PER_PAGE = 3
MAX_SEARCH_RESULTS = 50
