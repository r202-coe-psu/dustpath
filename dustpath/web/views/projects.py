from dustpath.models import projects
from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    Response,
    g,
    current_app,
    jsonify,
)
import datetime
from flask_login import login_required, current_user
import json
from dustpath import models
from dustpath.web import nats
from ..forms import ProjectForm

from .. import forms

module = Blueprint("projects", __name__, url_prefix="/projects")

@module.route('/')
def index():
    projects = models.Project.objects().order_by("-id")
    return render_template('projects/index.html',
                            projects=projects,)

@module.route('/create', methods=['GET', 'POST'])
def create():
    form = ProjectForm()
    form.domain.choices = get_domains_choices()
    if not form.validate_on_submit():
        return render_template('projects/create.html', form=form)
    project = models.Project(
        name=form.name.data,
        output_filename=f"wrfout_d01_{form.start_date.data}_00:00:00",
    )
    project.wrf_config.start_date = form.start_date.data
    project.wrf_config.end_date = form.end_date.data

    domain = models.Domain.objects.get(id=form.domain.data)
    project.wrf_config.domain = domain
    project.save()
    return redirect(url_for('projects.index'))
    
@module.route("/<project_id>/run_wrf", methods=["POST"])
def run_wrf(project_id):
    project = models.Project.objects.get(id=project_id)

    data = {
        "action": "start",
        # "user_id": str(current_user._get_current_object().id),
        "attributes": {
            "project_id": project_id,
            },
    }
    nats.nats_client.publish("dustpath.processor.command", data)
    
    return redirect(url_for('projects.result'))

@module.route('<project_id>/result', methods=['GET','POST'])
def result(project_id):
    project = models.Project.objects.get(id=project_id)
    return render_template('projects/result.html',
        project_id=project_id, 
        result=result, 
        project=project)

def get_domains_choices():
    domains = models.Domain.objects()
    return [(str(d.id), f"lat={d.center[0]}, lon={d.center[1]}, r={d.radius}") for d in domains]