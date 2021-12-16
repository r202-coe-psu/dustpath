from flask import (Blueprint,
                   Flask,
                   redirect,
                   render_template,
                   url_for,
                   current_app,
                   redirect)
from .. import models, forms
import datetime
import mongoengine as me
import pathlib
import subprocess

module = Blueprint('config', __name__, url_prefix='/config')

@module.route('/')
def index():
    return render_template('config/index.html',)
