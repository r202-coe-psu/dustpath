from flask import (Blueprint,
                   Flask,
                   redirect,
                   render_template,
                   url_for,
                   redirect)
from .. import models
import datetime
import mongoengine as me
import pathlib


module = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@module.route('/')
def index():
    return redirect(url_for('projects.index'))
