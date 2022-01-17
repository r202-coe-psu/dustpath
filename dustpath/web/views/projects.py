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
    if not form.validate_on_submit():
        return render_template('projects/create.html', form=form)
    project = models.Project(
        name=form.name.data,
        output_filename=f"wrfout_d01_{form.start_date.data}_00:00:00",
    )
    project.wrf_config.max_domain = form.max_domain.data
    project.wrf_config.start_date = form.start_date.data
    project.wrf_config.end_date = form.end_date.data
    project.save()
    # data = {
    #     "action": "create_project",
    #     "project_id": str(project.id),
    # }
    # nats.nats_client.publish("dustpath.storage.command", data)

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

    response = Response()
    response.status_code = 200
    return response

@module.route('<project_id>/result', methods=['GET','POST'])
def result(project_id):
    return render_template('projects/result.html', project_id=project_id)

# @module.route('/listresult', defaults={'req_path': ''})
# @module.route('/<path:req_path>')
# def listresult(req_path):
#     BASE_DIR = 'dustpath/static/gif'
#     # Joining the base and the requested path
#     abs_path = os.path.join(BASE_DIR, req_path)
#     files = os.listdir(abs_path)
#     return render_template('result/listresult.html', files=files)