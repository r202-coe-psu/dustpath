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

module = Blueprint('compile', __name__, url_prefix='/compile')

@module.route('/')
def index():
    # subprocess.Popen(['./activate'])
    return render_template('compile/index.html',)
