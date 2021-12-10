# import asyncio
# import datetime
# import json
# import pathlib
# import logging

# logger = logging.getLogger(__name__)

# from nats.aio.client import Client as NATS

# from dustpath import models
import shutil
import os

import wrf_running


class ControllerServer:
    def __init__(self):
        # self.settings = settings
        # models.init_mongoengine(settings)
        # self.nc = NATS()
        self.projects = {}
        self.projects_path = os.getcwd() + '/../projects/'
        self.mastery_project_path = self.projects_path + 'mastery_project/'

    def create_new_project(self, id):
        new_path = self.projects_path + str(id) + '/'
        if not os.path.exists(new_path):
            shutil.copytree(
                self.mastery_project_path, 
                new_path, 
                copy_function = shutil.copy
            )
        self.projects[id] = wrf_running.WRFRunningController(new_path)

    def run(self, id):
        print("---Start\n")
        if id not in self.projects.keys():
            self.create_new_project(id)
        print("start activate")
        self.projects[id].activate_container()
        print("activated")

        self.projects[id].run_geogrid()
        self.projects[id].link_gfs_file()
        self.projects[id].link_Vtable()
        self.projects[id].run_ungrib()
        self.projects[id].run_metgrid()
        self.projects[id].link_met_data()
        self.projects[id].run_real()
        self.projects[id].run_wrf()
        print("\n---End")

ControllerServer().run('9999')

