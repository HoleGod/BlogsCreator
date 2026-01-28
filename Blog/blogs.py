from flask import Blueprint, render_template, abort, request, redirect, url_for, current_app, flash, g
import datetime
from dotenv import load_dotenv, find_dotenv
from .utils import save_image, save_posts_list, save_post_dict
from .decortators import login_required
from .querys import get_all_posts, get_post, create_post_, update_post_

bp = Blueprint("blog", __name__)

load_dotenv(find_dotenv())

@bp.route('/')
def home():
	posts = get_all_posts()
	posts_list = save_posts_list(posts)

	return render_template('blog/blog.html', posts=posts_list)

@bp.route('/post/<int:post_id>')
@login_required
def show_post(post_id):
	post = get_post(post_id)
	if post is None:
		abort(404)
	post_dict = save_post_dict(post)
 
	return render_template('blog/post_detail.html', post=post_dict)

@bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
	if request.method == 'POST':
		title = request.form['title']
		short_description = request.form['short_description']
		content = request.form['content']
		date_posted = datetime.datetime.now()
		image_url = save_image(request.files.get('image')) 
		new_id = create_post_(title, short_description, content, date_posted, image_url, g.user['id'])
		
		return redirect(url_for('blog.show_post', post_id=new_id))
	return render_template('blog/create_post.html')

@bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
	post = get_post(post_id)

	if post is None:
		abort(404)

	if request.method == 'POST':
		title = request.form['title']
		short_description = request.form['short_description']
		content = request.form['content']
		image_url = post[4]
		image_file = request.files.get('image')
		image_url = save_image(image_file)
		update_post_(title, short_description, content, image_url, post_id)
		return redirect(url_for('blog.show_post', post_id=post_id))

	post_dict = save_post_dict(post)
	return render_template('blog/edit_post.html', post=post_dict)

@bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
	return redirect(url_for('blog.home'))