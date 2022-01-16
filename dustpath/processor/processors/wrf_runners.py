import datetime
import copy
import subprocess
import os
import sys

import logging
import threading

logger = logging.getLogger(__name__)


class WrfRunner(threading.Thread):
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
        # self.activate_path = path + 'activate'
        # self.wps_path = path + 'WPS/'
        # self.geogrid_path = self.wps_path + 'geogrid/'
        # self.geogrid_exe_path = self.wps_path + 'geogrid.exe'
        # self.ungrib_exe_path = self.wps_path + 'ungrib.exe'
        # self.metgrid_exe_path = self.wps_path + 'metgrid.exe'
        # self.link_gfs_exec_path = self.wps_path + 'link_grib.csh'
        # self.met_em_data_path = self.wps_path + 'met_em*'
        # self.gfs_data_path = path + '../../data/geo_data/gfs/fnl*'

        # self.wrf_path = path + 'WRF/no_emission_run/'
        # self.real_exe_path = self.wrf_path + 'real.exe'
        # self.wrf_exe_path = self.wrf_path + 'wrf.exe'

    def stop(self):
        self.running = False
    
    def link_geogrid_table(self):
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WPS/geogrid/ && \
            ln -svf GEOGRID.TBL.ARW_CHEM GEOGRID.TBL'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['link-geogrid-table'] = True
        else:
            self.running = False
        # return err_code

    def run_geogrid(self):
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WPS/ && ./geogrid.exe'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['run-geogrid'] = True
        else:
            self.running = False
        # return err_code

    def link_gfs_file(self):
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WPS/ && ./link_grib.csh ../data/geo_data/gfs/fnl*'",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
            
        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['link-gfs-file'] = True
        else:
            self.running = False

        # if res:
        #     print("out-->\n", res)

        # if err_code != 0:
        #     return res
        # return err_code
        
    def link_Vtable(self):
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WPS/ && ln -sf ungrib/Variable_Tables/Vtable.GFS Vtable'",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['link-Vtable'] = True
        else:
            self.running = False

        # if res:
        #     print("out-->\n", res)
        
        # if err_code != 0:
        #     return res
        # return err_code

    def run_ungrib(self):
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WPS/ && export LD_LIBRARY_PATH=/usr/local/lib:./ && ./ungrib.exe'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['run-ungrib'] = True
        else:
            self.running = False

        # if res:
        #     print("out-->\n", res)

        # if err_code != 0:
        #     return res
        # return err_code

    def run_metgrid(self):
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WPS/ && ./metgrid.exe'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['run-metgrid'] = True
        else:
            self.running = False

        # if res:
        #     print("out-->\n", res)

        # if err_code != 0:
        #     return res
        # return err_code
        
    def link_met_data(self):
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WRF/no_emission_run/ && ln -sf ../../WPS/met_em* .'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
            
        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['link-met-data'] = True
        else:
            self.running = False

        # if res:
        #     print("out-->\n", res)

        # if err_code != 0:
        #     return res
        # return err_code

    def run_real(self):
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WRF/no_emission_run/ && ./real.exe'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['run-real'] = True
        else:
            self.running = False

        # if res:
        #     print("res-->\n", res)

        # if err_code != 0:
        #     return res
        # return err_code

    def run_wrf(self):
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WRF/no_emission_run/ && ./wrf.exe'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['run-wrf'] = True
        else:
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
        