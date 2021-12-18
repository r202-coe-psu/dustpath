from dustpath.models import wrf_configs
from flask import (Blueprint,
                   Flask,
                   redirect,
                   render_template,
                   url_for,
                   current_app,
                   redirect)
from .. import models
from ..forms import WrfConfigForm
import datetime
import mongoengine as me

module = Blueprint('wrf_configs', __name__, url_prefix='/wrf_configs')

@module.route('/')
def index():
    wrf_configs = models.WrfConfig.objects().order_by("-id")
    return render_template('wrf_configs/index.html',
                            wrf_configs=wrf_configs,)

@module.route('/record', methods=['GET', 'POST'])
def record():
    form = WrfConfigForm()
    if not form.validate_on_submit():
        return render_template('wrf_configs/record.html', form=form)
    wrf_config = models.WrfConfig()
    form.populate_obj(wrf_config)
    wrf_config.save()

    return redirect(url_for('wrf_configs.index'))
