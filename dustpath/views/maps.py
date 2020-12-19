from flask import (Blueprint,
                   render_template,
                   redirect,
                   url_for,
                   request,
                   jsonify
                   )
import json, datetime
from flask_login import login_required
from .. import models

module = Blueprint('maps', __name__, url_prefix='/maps')

@module.route('/')
def index():
    popup_id = request.args.get('id')
    center = [6.37, 101.4] # lat, long
    zoom = 10
    
    return render_template('maps/index.html',
                           zoom=zoom,
                           center=center,
                           popup_id=popup_id)