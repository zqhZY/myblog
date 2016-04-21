 #encoding=utf-8

from models import User, Tag, Post, Category, tag_entry
from __init__ import db

class DataWrappers(object):

    def get_all_entries(self):
        return Post.query.all()

    def get_prev_entry(self, id):
        ent = db.engine.execute('SELECT * FROM  `post`  where id < %s  order by create_time desc' % id).first()
        return ent

    def get_next_entry(self, id):
        ent = db.engine.execute('SELECT * FROM  `post`  where id>%s  order by create_time asc ' % id).first()
        return ent

    def get_entry_by_category(self, categories):
        counts = []
        for category in categories:
            counts.append(Post.query.filter_by(category=category).count())

        return counts


    def increase_view_count(self, post, num):
        post.view_count += num
        db.session.commit()
        return None

    def get_entries_by_page(self, page, par_page):
        pages = Post.query.order_by(Post.create_time.desc()).paginate(page, par_page)
        return pages

    def get_entry_by_id(self, id):
        ent = Post.query.get(id)
        return ent

    def get_all_tags(self):
        ts = Tag.query.all()
        return ts

    def get_all_categories(self):
        categories = Category.query.all()
        return categories

    def get_category_by_id(self, id):
        cate = Category.query.get(id)
        return cate

    def get_tag_by_id(self, id):
        tag = Tag.query.get(id)
        return tag
'''
    def get_all_links(self):
        links = Friend_link.query.all()
        return links

    def get_first_user(self):
        user = User.query.all()
        return user
'''
