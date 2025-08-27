from flask import Blueprint, render_template, abort, request, redirect, url_for, current_app, flash, g
from werkzeug.utils import secure_filename
import os
import datetime
import time
import psycopg2
from dotenv import load_dotenv, find_dotenv

bp = Blueprint("blog", __name__)

load_dotenv(find_dotenv())

def get_db_connection():
    return psycopg2.connect(
		port=5432,
		host=os.getenv('HOST'),
		dbname=os.getenv('DBNAME'),
		user=os.getenv('DB_USERNAME'),
		password=os.getenv('DB_PASSWORD')
	)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def home():
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute("SELECT id, title, short_description, date_posted, image, content FROM post ORDER BY date_posted DESC")
	posts = cur.fetchall()
	cur.close()
	conn.close()

	posts_list = []
	for p in posts:
		posts_list.append({
			'id': p[0],
			'title': p[1],
			'short_description': p[2],
			'date': p[3].strftime('%Y-%m-%d') if p[3] else '',
			'image': p[4],
			'content': p[5]
		})

	return render_template('blog/blog.html', posts=posts_list)

@bp.route('/post/<int:post_id>')
def show_post(post_id):
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute('''
		SELECT post.id, post.title, post.short_description, post.date_posted, post.image, post.content, users.username 
		FROM post 
		JOIN users ON post.user_id = users.id
		WHERE post.id = %s
	''', (post_id,))
	post = cur.fetchone()
	cur.close()
	conn.close()

	if post is None:
		abort(404)

	post_dict = {
		'id': post[0],
		'title': post[1],
		'short_description': post[2],
		'date': post[3].strftime('%Y-%m-%d'),
		'image': post[4],
		'content': post[5],
		'author': post[6]
	}

	return render_template('blog/post_detail.html', post=post_dict)

@bp.route('/post/create', methods=['GET', 'POST'])
def create_post():
	if request.method == 'POST':
		if g.user is None:
			flash("You must log in to create posts!")
			return redirect(url_for("auth.login"))

		title = request.form['title']
		short_description = request.form['short_description']
		content = request.form['content']
		date_posted = datetime.datetime.now()

		image_file = request.files.get('image')
		if image_file and allowed_file(image_file.filename):
			filename = secure_filename(image_file.filename)
			name, ext = os.path.splitext(filename)
			unique_name = f"{name}_{int(time.time())}{ext}"
			upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
			os.makedirs(upload_folder, exist_ok=True) 
			image_path = os.path.join(upload_folder, unique_name)
			image_file.save(image_path)
			image_url = 'uploads/' + unique_name 
		else:
			image_url = 'uploads/default.png' 

		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute(
			'INSERT INTO post (title, short_description, content, image, date_posted, user_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
			(title, short_description, content, image_url, date_posted, g.user['id'])
		)
		new_id = cur.fetchone()[0]
		conn.commit()
		cur.close()
		conn.close()
		return redirect(url_for('blog.show_post', post_id=new_id))
	return render_template('blog/create_post.html')
@bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
	conn = get_db_connection()
	cur = conn.cursor()
	
	cur.execute('SELECT id, title, short_description, content, image FROM post WHERE id = %s', (post_id,))
	post = cur.fetchone()

	if post is None:
		cur.close()
		conn.close()
		abort(404)

	if request.method == 'POST':
		title = request.form['title']
		short_description = request.form['short_description']
		content = request.form['content']
		image_url = post[4]

		image_file = request.files.get('image')
		if image_file and allowed_file(image_file.filename):
			filename = secure_filename(image_file.filename)
			name, ext = os.path.splitext(filename)
			unique_name = f"{name}_{int(time.time())}{ext}"
			upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
			os.makedirs(upload_folder, exist_ok=True)
			image_path = os.path.join(upload_folder, unique_name)
			image_file.save(image_path)
			image_url = 'uploads/' + unique_name

		cur.execute(
			'UPDATE post SET title = %s, short_description = %s, content = %s, image = %s WHERE id = %s',
			(title, short_description, content, image_url, post_id)
		)

		conn.commit()
		cur.close()
		conn.close()

		return redirect(url_for('blog.show_post', post_id=post_id))

	cur.close()
	conn.close()

	post_dict = {
		'id': post[0],
		'title': post[1],
		'short_description': post[2],
		'content': post[3],
		'image': post[4]
	}

	return render_template('blog/edit_post.html', post=post_dict)


@bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
	conn = get_db_connection()
	cur = conn.cursor()

	cur.execute('DELETE FROM post WHERE id = %s', (post_id,))
	conn.commit()
	cur.close()
	conn.close()

	return redirect(url_for('blog.home'))