from dustpath.models import domains
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

module = Blueprint('domains', __name__, url_prefix='/domains')

@module.route('/')
def index():
    domains = models.Domain.objects().order_by("-id")
    return render_template('domains/index.html',
                            domains=domains,)

@module.route('/record', methods=['GET', 'POST'])
def record():
    center = [7.0065949668769205, 100.49891880632555] # lat, long
    zoom = 10
    
    if request.method == 'POST':
        data = request.json
        if data:
            domain = models.Domain(
                name=data['name'],
                center=data['center'],
                width=data['width'],
                hight=data['hight'],
                dx=data['width']/100,
                dy=data['hight']/100,
                e_we=100,
                e_sn=100,
                )
            area = (domain.dx / 1000) * (domain.dy / 1000) * 10000
            if domain.dx < domain.dy:
                domain.dy = domain.dx
                resolution = (domain.dx / 1000) * (domain.dy / 1000)
                domain.e_sn = (area / resolution) / 100
            elif domain.dy < domain.dx:
                domain.dX = domain.dy
                resolution = (domain.dx / 1000) * (domain.dy / 1000)
                domain.e_we = (area / resolution) / 100
            domain.save()
    return render_template('domains/record.html',
                           zoom=zoom,
                           center=center,)