from flask import Flask
from Blog import blogs, pages, info
import os

def create_app():

    app = Flask(__name__)
    app.secret_key=os.getenv('SECRET_KEY')
    app.register_blueprint(pages.bp)
    app.register_blueprint(blogs.bp)
    app.register_blueprint(info.bp)

    return app

#frg56454#