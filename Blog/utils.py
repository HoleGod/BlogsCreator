from flask import current_app
from werkzeug.utils import secure_filename
import os
import time

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(image_file):
	image_url = "uploads/default.png"
	if image_file and allowed_file(image_file.filename):
		filename = secure_filename(image_file.filename)
		name, ext = os.path.splitext(filename)
		unique_name = f"{name}_{int(time.time())}{ext}"
		upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
		os.makedirs(upload_folder, exist_ok=True)
		image_path = os.path.join(upload_folder, unique_name)
		image_file.save(image_path)
		image_url = 'uploads/' + unique_name
	return image_url

def save_posts_list(posts):
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
	return posts_list

def save_post_dict(post):
	post_dict = {
		'id': post[0],
		'title': post[1],
		'short_description': post[2],
		'date': post[3].strftime('%Y-%m-%d'),
		'image': post[4],
		'content': post[5],
		'author': post[6]
	}
	
	return post_dict

def user_to_g(user_row):
	if not user_row:
		return None
	return {
		"id": user_row[0],
		"username": user_row[1]
	}
