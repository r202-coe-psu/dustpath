import datetime
import copy
import subprocess
import os
import sys
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import matplotlib as mpl
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
from matplotlib.colors import LinearSegmentedColormap
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)

import logging
import threading

logger = logging.getLogger(__name__)


class Plotter(threading.Thread):
    def __init__(self, project_path, data_path):
        super().__init__()
        self.running = False
        self.user = '${USER}'
        self.status = {
            'link-geogrid-table': False, 
            'run-geogrid': False, 
            'link-gfs-file': False,
            'link-Vtable': False, 
            'run-ungrib': False, 
            'run-metgrid': False,
            'link-met-data': False, 
            'run-real': False, 
            'run-wrf': False,
            }
        self.project_path = project_path
        self.data_path = data_path
        self.ncfile = Dataset("wrfout_d03_2019-09-10_newfirererun.nc")

    def stop(self):
        self.running = False

    def run(self):
        logger.debug("Start Wrf Runner")
        self.running = True
        logger.debug(f'link_geogrid_table')
        self.link_geogrid_table()
        if self.status['link-geogrid-table']:
            logger.debug(f'run_geogrid')
            self.run_geogrid()
        if self.status['run-geogrid']:
            logger.debug(f'link_gfs_file')
            self.link_gfs_file()
        if self.status['link-gfs-file']:
            logger.debug(f'link_Vtable')
            self.link_Vtable()
        if self.status['link-Vtable']:
            logger.debug(f'run_ungrib')
            self.run_ungrib()
        if self.status['run-ungrib']:
            logger.debug(f'run_metgrid')
            self.run_metgrid()
        if self.status['run-metgrid']:
            logger.debug(f'link_met_data')
            self.link_met_data()
        if self.status['link-met-data']:
            logger.debug(f'run_real')
            self.run_real()
        if self.status['run-real']:
            logger.debug(f'run_wrf')
            self.run_wrf()
        self.running = False
        logger.debug("Start Wrf Runner")
        