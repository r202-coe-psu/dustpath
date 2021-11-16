from flask import (Blueprint,
                   Flask,
                   redirect,
                   render_template,
                   url_for,
                   current_app,
                   redirect)
from .. import models
import datetime
import mongoengine as me
import pathlib
import subprocess

module = Blueprint('compile', __name__, url_prefix='/compile')

@module.route('/')
def index():
    subprocess.Popen(['./activate'])
    return redirect(url_for('dashboard.index'))
