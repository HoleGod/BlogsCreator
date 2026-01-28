from .db import get_db_connection

def get_all_posts():
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute("SELECT id, title, short_description, date_posted, image, content FROM post ORDER BY date_posted DESC")
	posts = cur.fetchall()
	cur.close()
	conn.close()

	return posts

def get_post(post_id):
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
	
	return post

def create_post_(title, short_description, content, date_posted, image_url, id):
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		'INSERT INTO post (title, short_description, content, image, date_posted, user_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
		(title, short_description, content, image_url, date_posted, id)
	)
	new_id = cur.fetchone()[0]
	conn.commit()
	cur.close()
	conn.close()
	
	return new_id

def detele_post_(post_id):
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute('DELETE FROM post WHERE id = %s', (post_id,))
	conn.commit()
	cur.close()
	conn.close()
 
def update_post_(title, short_description, content, image_url, id):
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
			'UPDATE post SET title = %s, short_description = %s, content = %s, image = %s WHERE id = %s',
			(title, short_description, content, image_url, id)
		)
	conn.commit()
	cur.close()
	conn.close()
 
def get_user_by_id(user_id):
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"SELECT id, username FROM users WHERE id = %s",
		(user_id,)
	)
	user = cur.fetchone()
	cur.close()
	conn.close()
	return user

def get_user_by_username(username):
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"SELECT id, username, password_hash FROM users WHERE username = %s",
		(username,)
	)
	user = cur.fetchone()
	cur.close()
	conn.close()
	return user

def create_user(username, password_hash):
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute(
		"INSERT INTO users (username, password_hash) VALUES (%s, %s)",
		(username, password_hash)
	)
	conn.commit()
	cur.close()
	conn.close()