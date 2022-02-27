
from importlib.resources import path
import pathlib
import subprocess
import shutil
import os

import logging
import threading
import jinja2
import json

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
from PIL import Image, ImageDraw

logger = logging.getLogger(__name__)


class WrfRunner(threading.Thread):
    def __init__(self, setting, attributes):
        super().__init__()
        self.settings = setting
        self.running = False
        self.user = '${USER}'
        self.status = {
            'copy-project': '',
            'write-namelist-wps': '',
            'link-geogrid-table': '', 
            'run-geogrid': '', 
            'link-gfs-file': '',
            'link-Vtable': '', 
            'run-ungrib': '', 
            'run-metgrid': '',
            'link-met-data': '', 
            'write-no-emiss-namelist-input': '',
            'run-real-1': '', 
            'write-prep-chem-src-input': '',
            'run-prep-chem-src': '', 
            'link-prep-chem-src': '',
            'write-emiss-namelist-input': '',
            'convert-emission': '', 
            'link-chemi': '',
            'run-real-2': '', 
            'run-wrf': '',
            'plot': '', 
            'generate-GIF': '',
            }

        self.project_id = attributes.get('project_id')
        self.namelist_wps = attributes.get('namelist_wps')
        self.no_emiss_namelist_input = attributes.get('no_emiss_namelist_input')
        self.emiss_namelist_input = attributes.get('emiss_namelist_input')
        self.prep_chem_src_input = attributes.get('prep_chem_sources_input')
        self.output_file = attributes.get('output_file')
        self.days = attributes.get('days')

        self.projects_path = pathlib.Path(
                self.settings.get("DUSTPATH_PROCESSOR_CACHE_PATH", '/tmp')
                )
        self.data_path = pathlib.Path(
                self.settings.get("DUSTPATH_PROCESSOR_WRF_DATA_PATH")
                )
        self.mastery_project_path = self.projects_path / pathlib.Path('mastery_project')

        self.project_path = self.projects_path / pathlib.Path(self.project_id)
        self.wps_path = self.project_path / 'WPS'
        self.wrf_path = self.project_path / 'WRF/run'
        self.prep_chem_src_path = self.project_path / 'PREP-CHEM-SRC-1.5/bin'
        self.pic_path = self.project_path / 'WRF/run/pic'
        self.gif_path = pathlib.Path(
                self.settings.get("DUSTPATH_GIF_PATH")) / self.project_id

    def stop(self):
        self.running = False

    def copy_project(self):
        self.status['copy-project'] = 'running'
        try:
            if not os.path.exists(self.project_path):
                shutil.copytree(
                    self.mastery_project_path, 
                    self.project_path,
                    symlinks=True,
                    copy_function = shutil.copy
                )
            self.status['copy-project'] = 'success'
        except Exception as e:
            logger.debug(e)
            self.status['copy-project'] = 'fail'
            self.running = False
                    
    def write_namelist_wps(self):
        self.status['write-namelist-wps'] = 'running'
        try:
            f = open(self.wps_path / "namelist.wps" , "w")
            f.write(json.loads(self.namelist_wps))
            f.close()
            self.status['write-namelist-wps'] = 'success'
        except Exception as e:
            logger.debug(e)
            self.status['write-namelist-wps'] = 'fail'
            self.running = False
    
    def link_geogrid_table(self):
        self.status['link-geogrid-table'] = 'running'
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
            self.status['link-geogrid-table'] = 'success'
        else:
            self.status['link-geogrid-table'] = 'fail'
            self.running = False
            
    def run_geogrid(self):
        self.status['run-geogrid'] = 'running'
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
            self.status['run-geogrid'] = 'success'
        else:
            self.status['run-geogrid'] = 'fail'
            self.running = False

    def link_gfs_file(self):
        self.status['link-gfs-file'] = 'running'
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
            self.status['link-gfs-file'] = 'success'
        else:
            self.status['link-gfs-file'] = 'fail'
            self.running = False
        
    def link_Vtable(self):
        self.status['link-Vtable'] = 'running'
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
            self.status['link-Vtable'] = 'success'
        else:
            self.status['link-Vtable'] = 'fail'
            self.running = False

    def run_ungrib(self):
        self.status['run-ungrib'] = 'running'
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
            self.status['run-ungrib'] = 'success'
        else:
            self.status['run-ungrib'] = 'fail'
            self.running = False

    def run_metgrid(self):
        self.status['run-metgrid'] = 'running'
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WPS/ && mpirun --oversubscribe -np 7 ./metgrid.exe'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['run-metgrid'] = 'success'
        else:
            self.status['run-metgrid'] = 'fail'
            self.running = False
        
    def link_met_data(self):
        self.status['link-met-data'] = 'running'
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WRF/run/ && ln -sf ../../WPS/met_em* .'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
            
        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['link-met-data'] = 'success'
        else:
            self.status['link-met-data'] = 'fail'
            self.running = False
                    
    def write_no_emiss_namelist_input(self):
        self.status['write-no-emiss-namelist-input'] = 'running'
        try:
            f = open(self.wrf_path / "namelist.input" , "w")
            f.write(json.loads(self.no_emiss_namelist_input))
            f.close()
            self.status['write-no-emiss-namelist-input'] = 'success'
        except Exception as e:
            logger.debug(e)
            self.status['write-no-emiss-namelist-input'] = 'fail'
            self.running = False

    def run_real_1(self):
        self.status['run-real-1'] = 'running'
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WRF/run/ && ./real.exe'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['run-real-1'] = 'success'
        else:
            self.status['run-real-1'] = 'fail'
            self.running = False

    def write_prep_chem_src_input(self):
        self.status['write-prep-chem-src-input'] = 'running'
        try:
            f = open(self.prep_chem_src_path / "prep_chem_sources.inp" , "w")
            f.write(json.loads(self.prep_chem_src_input))
            f.close()
            self.status['write-prep-chem-src-input'] = 'success'
        except Exception as e:
            logger.debug(e)
            self.status['write-prep-chem-src-input'] = 'fail'
            self.running = False
                    
    def run_prep_chem_src(self):
        self.status['run-prep-chem-src'] = 'running'
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd PREP-CHEM-SRC-1.5/bin/ && \
            rm -rf matrixfire* && \
            ./prep_chem_sources_RADM_WRF_FIM_.exe < prep_chem_sources.inp'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['run-prep-chem-src'] = 'success'
        else:
            self.status['run-prep-chem-src'] = 'fail'
            self.running = False
                    
    def link_prep_chem_src(self):
        self.status['link-prep-chem-src'] = 'running'
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WRF/run/ && \
                ln -sf ../../PREP-CHEM-SRC-1.5/bin/*-ab.bin emissopt3_d01 && \
                ln -sf ../../PREP-CHEM-SRC-1.5/bin/*-bb.bin emissfire_d01 && \
                ln -sf ../../PREP-CHEM-SRC-1.5/bin/*-gocartBG.bin wrf_gocart_backg'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['link-prep-chem-src'] = 'success'
        else:
            self.status['link-prep-chem-src'] = 'fail'
            self.running = False

    def write_emiss_namelist_input(self):
        self.status['write-emiss-namelist-input'] = 'running'
        try:
            f = open(self.wrf_path / "namelist.input" , "w")
            f.write(json.loads(self.emiss_namelist_input))
            f.close()
            self.status['write-emiss-namelist-input'] = 'success'
        except Exception as e:
            logger.debug(e)
            self.status['write-emiss-namelist-input'] = 'fail'
            self.running = False

    def convert_emission(self):
        self.status['convert-emission'] = 'running'
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WRF/run/ && ./convert_emiss.exe'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['convert-emission'] = 'success'
        else:
            self.status['convert-emission'] = 'fail'
            self.running = False
                    
    def link_chemi(self):
        self.status['link-chemi'] = 'running'
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WRF/run/ && \
                ln -sf wrfchemi_d01 wrfchemi_12z_d01 && \
                ln -sf wrfchemi_d01 wrfchemi_00z_d01 '",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['link-chemi'] = 'success'
        else:
            self.status['link-chemi'] = 'fail'
            self.running = False
    
    def run_real_2(self):
        self.status['run-real-2'] = 'running'
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WRF/run/ && ./real.exe'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['run-real-2'] = 'success'
        else:
            self.status['run-real-2'] = 'fail'
            self.running = False

    def run_wrf(self):
        self.status['run-wrf'] = 'running'
        self.process = subprocess.Popen(
            f"docker run --rm --shm-size=2048M \
            -v {self.project_path}:/home/{self.user}/projects \
            -v {self.data_path}:/home/{self.user}/projects/data \
            wrf-image /bin/sh -c \
            'cd WRF/run/ && mpirun --oversubscribe -np 7 ./wrf.exe'",
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        res = self.process.communicate()
        err_code = self.process.returncode
        logger.debug(f'response: {res}')
        logger.debug(f'err-code: {err_code}')
        if not err_code:
            self.status['run-wrf'] = 'success'
        else:
            self.status['run-wrf'] = 'fail'
            self.running = False
    
    def plot(self):
        self.status['plot'] = 'running'

        try:
            ncfile = Dataset(pathlib.Path(self.wrf_path / self.output_file))
            cm = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', ['#00c7ff' , '#6ee44b', '#f1ff00', '#ffa500', '#ff0024'], 1024)
            hours = np.arange(0, 24*self.days)

            for i in hours:
                # PM2_5_DRY = getvar(ncfile, "PM2_5_DRY", timeidx=i)[0,:]
                PM2_5 = getvar(ncfile, "PM2_5_DRY", timeidx=i)[0,:]

                cart_proj = get_cartopy(PM2_5)
                lats, lons = latlon_coords(PM2_5)


                fig = plt.figure(figsize=(19,12))


                ax = plt.axes(projection=crs.PlateCarree())
                # ax.set_global()
                # ax.set_extent([90, 110 , 0, 20])
                # ax.stock_img()
                ax.coastlines(linewidth=0.5)

                # lvl = np.arange(990, 1030, 2.5)

                plt.contourf(lons,
                            lats,
                            PM2_5,
                            # level=lvl,
                            transform=crs.PlateCarree(),
                            #cmap=plt.get_cmap('jet'))
                            cmap=cm)
                t = np.datetime64(PM2_5.Time.values)
                date = np.datetime_as_string(t, unit='D')
                plt.title('PM2.5 : ' + date)

                axs, _ = mpl.colorbar.make_axes(plt.gca(), shrink=0.5)  

                cbar = mpl.colorbar.ColorbarBase(axs, cmap=cm,
                                norm=mpl.colors.Normalize(vmin=-0, vmax=100))

                path = pathlib.Path(self.pic_path)
                if not path.exists() and not path.is_dir():
                    path.mkdir(parents=True)

                plt.savefig(
                    pathlib.Path(f"{self.pic_path}") / pathlib.Path(str(i)+'.jpg'))
                # plt.show()
            self.status['plot'] = 'success'
        except Exception as e:
            logger.debug(e)
            self.status['plot'] = 'fail'
            self.running = False
    
    def genarate_GIF_file(self):
        self.status['generate-GIF'] = 'running'
        try:
            image_frames=[]

            hours = np.arange(0, 24*self.days)

            for i in hours:
                new_frame = Image.open(
                    pathlib.Path(f"{self.pic_path}") / pathlib.Path(str(i)+'.jpg'))
                image_frames.append(new_frame)

            path = pathlib.Path(self.gif_path)
            if not path.exists() and not path.is_dir():
                path.mkdir(parents=True)

            image_frames[0].save(
                pathlib.Path(f"{path}/output.gif"), 
                format = 'GIF', append_images = image_frames[1: ], save_all = True, duration = 300, loop = 0) 
            self.status['generate-GIF'] = 'success'
        except Exception as e:
            logger.debug(e)
            self.status['generate-GIF'] = 'fail'
            self.running = False

    def run(self):
        logger.debug("Start Wrf Runner")
        self.running = True
        logger.debug(f'copy_project')
        self.copy_project()
        if self.status['copy-project'] == 'success':
            logger.debug(f'write_namelist_wps')
            self.write_namelist_wps()
        if self.status['write-namelist-wps'] == 'success':
            logger.debug(f'link_geogrid_table')
            self.link_geogrid_table()
        if self.status['link-geogrid-table'] == 'success':
            logger.debug(f'run_geogrid')
            self.run_geogrid()
        if self.status['run-geogrid'] == 'success':
            logger.debug(f'link_gfs_file')
            self.link_gfs_file()
        if self.status['link-gfs-file'] == 'success':
            logger.debug(f'link_Vtable')
            self.link_Vtable()
        if self.status['link-Vtable'] == 'success':
            logger.debug(f'run_ungrib')
            self.run_ungrib()
        if self.status['run-ungrib'] == 'success':
            logger.debug(f'run_metgrid')
            self.run_metgrid()
        if self.status['run-metgrid'] == 'success':
            logger.debug(f'link_met_data')
            self.link_met_data()
        if self.status['link-met-data'] == 'success':
            logger.debug(f'write_no_emiss_namelist_input')
            self.write_no_emiss_namelist_input()
        if self.status['write-no-emiss-namelist-input'] == 'success':
            logger.debug(f'run_real_1')
            self.run_real_1()
        if self.status['run-real-1'] == 'success':
            logger.debug(f'write_prep_chem_src_input')
            self.write_prep_chem_src_input()
        if self.status['write-prep-chem-src-input'] == 'success':
            logger.debug(f'run-prep-chem-src')
            self.run_prep_chem_src()
        if self.status['run-prep-chem-src'] == 'success':
            logger.debug(f'link-prep-chem-src')
            self.link_prep_chem_src()
        if self.status['link-prep-chem-src'] == 'success':
            logger.debug(f'write-emiss-namelist-input')
            self.write_emiss_namelist_input()
        if self.status['write-emiss-namelist-input'] == 'success':
            logger.debug(f'convert-emission')
            self.convert_emission()
        if self.status['convert-emission'] == 'success':
            logger.debug(f'link-chemi')
            self.link_chemi()
        if self.status['link-chemi'] == 'success':
            logger.debug(f'run-real-2')
            self.run_real_2()
        if self.status['run-real-2'] == 'success':
            logger.debug(f'run_wrf')
            self.run_wrf()
        if self.status['run-wrf'] == 'success':
            logger.debug(f'plot')
            self.plot()
        if self.status['plot'] == 'success':
            logger.debug(f'genarate_GIF_file')
            self.genarate_GIF_file()
        logger.debug("finish Wrf Runner And wait for get status")
        