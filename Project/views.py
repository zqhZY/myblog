
#encoding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from datetime import datetime
from __init__ import app , db
#from forms import  SearchForm
from models import User, Post

from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS

from data_wrappers import DataWrappers

data_wrap = DataWrappers()


@app.before_request
def before_request():
	#g.search_form = SearchForm()
	g.user = current_user
    
@app.teardown_request
def teardown_request(response_or_exc):
    db.session.remove()
    

'''
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()
'''

#main page process
@app.route('/')
@app.route('/blog')
@app.route('/blog/<int:page>')
def show_blog(page=1):

	if page < 1:
		page = 1
	p = data_wrap.get_entries_by_page(page=page, par_page=POSTS_PER_PAGE)

	#p = Post.query.order_by(Post.create_time.desc()).paginate(page, 3)
	entries = p.items		
	
	if not p.total:
		pagination = [0]		
	elif p.total %POSTS_PER_PAGE != 0:
		pagination = range(1, p.total/POSTS_PER_PAGE + 2)	    
	else:	
		pagination = range(1, p.total/POSTS_PER_PAGE + 1)

	return render_template('HomePage.html', entries=entries,
			p=p, page=page, pagination=pagination,
			)


@app.route('/entry/<int:entry_id>')
def show_entry(entry_id):
    entry = data_wrap.get_entry_by_id(entry_id)
    data_wrap.increase_view_count(entry, 1)
    return render_template('Post_display.html', entry=entry,
                            )

@app.route('/entry/<int:entry_id>/prev')
def prev_entry(entry_id):
    entry = data_wrap.get_prev_entry(entry_id)
    if entry is None:
        return redirect(url_for('Post_display.html', entry_id=entry_id))
    return redirect(url_for('Post_display.html', entry_id=entry.id))


@app.route('/entry/<int:entry_id>/next')
def next_entry(entry_id):
    entry = data_wrap.get_next_entry(entry_id)
    if entry is None:
        return redirect(url_for('Post_display.html', entry_id=entry_id))
    return redirect(url_for('Post_display.html', entry_id=entry.id))


@app.route('/all_category')
def all_category_display():
	categorys = data_wrap.get_all_categories()
	return render_template('all_category_display.html' , categorys = categorys)


@app.route('/category/<int:category_id>')
def category_display(category_id):
    category = data_wrap.get_category_by_id(category_id)
    return render_template('Category_display.html', category=category
                           )
@app.route('/about')
def about_display():
    return render_template('About_display.html')

@app.route('/comment')
def comment_display():
	return render_template('Comment_display.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


'''
@app.route('/search', methods=['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('show_blog'))
    return redirect(url_for('search_results', query=g.search_form.search.data))


@app.route('/search_results/<query>')
def search_results(query):
    
	results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    
	return render_template('search_results.html',
                           query=query,
						   results = results,
						   )
'''