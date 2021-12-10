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
    form = forms.BodyControlForm()
    if not form.validate_on_submit():
        print(form.errors)
        return render_template('compile/index.html',
                            form=form,
                            settings=settings)
    return render_template('compile/index.html',
                           form=form,)
