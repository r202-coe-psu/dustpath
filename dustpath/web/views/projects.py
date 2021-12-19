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

@module.route('/record', methods=['GET', 'POST'])
def create():
    form = ProjectForm()
    if not form.validate_on_submit():
        return render_template('projects/create.html', form=form)
    project = models.Project(
        name=form.name.data,
    )
    project.wrf_config.max_domain = form.max_domain.data
    project.wrf_config.start_date = form.start_date.data
    project.wrf_config.end_date = form.end_date.data
    project.save()

    return redirect(url_for('projects.index'))
    
@module.route("/<project_id>/run_wrf", methods=["POST"])
def run_wrf(project_id):
    project_id = request.form.get("project_id")
    project = models.Project.objects.get(id=project_id)
    # if not project.is_assistant_or_owner(current_user._get_current_object()):
    #     return Response(403)

    # camera = models.Camera.objects.get(id=camera_id)
    data = {
        "action": "start-recorder",
        # "camera_id": camera_id,
        "project_id": project_id,
        # "user_id": str(current_user._get_current_object().id),
    }

    # if camera.motion_property.active:
    #     data["motion"] = camera.motion_property.active
    #     data["sensitivity"] = camera.motion_property.sensitivity

    nats.nats_client.publish("dustpath.processor.command", data)

    response = Response()
    response.status_code = 200
    return response