
import jinja2
import logging
import os
logger = logging.getLogger(__name__)
import pathlib
import json


class ConfigurationComposer:
    def __init__(self, setting):
        self.setting = setting
        self.template_dir = pathlib.Path(pathlib.Path.cwd() / "dustpath/web/static/namelists/")

    def get_namelist_wps(self, project):
        loader = jinja2.FileSystemLoader(self.template_dir)
        env = jinja2.Environment(loader=loader,)
        template = env.get_template('namelist_wps.j2')
        
        result = template.render(wrf_config=project.wrf_config)
        return json.dumps(result) 

    def get_namelist_input(self, project):
        loader = jinja2.FileSystemLoader(self.template_dir)
        env = jinja2.Environment(loader=loader)
        template = env.get_template('namelist_input.j2')
        delta = project.wrf_config.end_date - project.wrf_config.start_date

        result = template.render(wrf_config=project.wrf_config, days=delta.days)
        return json.dumps(result) 