import logging

from flask import current_app, Flask, redirect, url_for

def create_app():
    application = Flask(__name__)
    return application
