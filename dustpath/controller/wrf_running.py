# from monthong import models

import logging
import datetime
import copy
import subprocess
import os
import sys

logger = logging.getLogger(__name__)


class WRFRunningController:
    def __init__(self, path):
        self.path = path
        self.activate_path = path + 'activate'
        self.wps_path = path + 'WPS/'
        self.geogrid_path = self.wps_path + 'geogrid/'
        self.geogrid_exe_path = self.wps_path + 'geogrid.exe'
        self.ungrib_exe_path = self.wps_path + 'ungrib.exe'
        self.metgrid_exe_path = self.wps_path + 'metgrid.exe'
        self.link_gfs_exec_path = self.wps_path + 'link_grib.csh'
        self.met_em_data_path = self.wps_path + 'met_em*'
        self.gfs_data_path = path + '../../data/geo_data/gfs/fnl*'

        self.wrf_path = path + 'WRF/no_emission_run/'
        self.real_exe_path = self.wrf_path + 'real.exe'
        self.wrf_exe_path = self.wrf_path + 'wrf.exe'

    def activate_container(self):
        activate_process = subprocess.Popen([
            self.activate_path
            ],
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        
    def run_geogrid(self):
        tbl_process = subprocess.run([
            "ln", 
            "-svf", 
            "GEOGRID.TBL.ARW_CHEM", 
            "GEOGRID.TBL"],
            cwd=self.geogrid_path,
            capture_output=True, 
            text=True
        )
        print(tbl_process.stdout)

        geogrid_process = subprocess.Popen([
            self.geogrid_exe_path
            ],
            cwd=self.wps_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        res = geogrid_process.communicate()
        err_code = geogrid_process.returncode

        if res:
            print("out-->\n", res)

    def link_gfs_file(self):
        link_grib_process = subprocess.Popen([
            self.link_gfs_exec_path,
            self.gfs_data_path,
            ],
            cwd=self.wps_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        res = link_grib_process.communicate()
        err_code = link_grib_process.returncode

        if res:
            print("out-->\n", res)

        if err_code != 0:
            return res
        
    def link_Vtable(self):
        link_process = subprocess.run([
            "ln", 
            "-sf", 
            "ungrib/Variable_Tables/Vtable.GFS", 
            "Vtable"],
            cwd=self.wps_path,
            capture_output=True, 
            text=True)
        # print(link_process.stdout)
        # res = link_process.communicate()
        # err_code = link_process.returncode

        # if res:
        #     print("out-->\n", res)
        
        # if err_code != 0:
        #     return res

    def run_ungrib(self):
        ungrib_process = subprocess.Popen([
            self.ungrib_exe_path,
            ],
            cwd=self.wps_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        res = ungrib_process.communicate()
        err_code = ungrib_process.returncode

        if res:
            print("out-->\n", res)

        if err_code != 0:
            return res

    def run_metgrid(self):
        metgrid_process = subprocess.Popen([
            self.metgrid_exe_path,
            ],
            cwd=self.wps_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        res = metgrid_process.communicate()
        err_code = metgrid_process.returncode

        if res:
            print("out-->\n", res)

        if err_code != 0:
            return res
        
    def link_met_data(self):
        link_process = subprocess.run([
            "ln", 
            "-sf", 
            self.met_em_data_path,
            "."],
            cwd=self.wrf_path,
            capture_output=True, 
            text=True)
        # print(link_process.stdout)
        # res = link_process.communicate()
        # err_code = link_process.returncode

        # if res:
        #     print("out-->\n", res)
        
        # if err_code != 0:
        #     return res

    def run_real(self):
        real_process = subprocess.Popen([
            self.real_exe_path,
            ],
            cwd=self.wrf_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        res = real_process.communicate()
        err_code = real_process.returncode

        if res:
            print("res-->\n", res)

        if err_code != 0:
            return res

    def run_wrf(self):
        wrf_process = subprocess.Popen([
            self.wrf_exe_path,
            ],
            cwd=self.wrf_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        res = wrf_process.communicate()
        err_code = wrf_process.returncode

        if res:
            print("out-->\n", res)

        if err_code != 0:
            return res