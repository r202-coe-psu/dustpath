import datetime
import copy
import pathlib
import subprocess
import os
import sys

import logging
import threading

logger = logging.getLogger(__name__)


class WrfRunner(threading.Thread):
    def __init__(self, project_path, data_path, project_id, setting):
        super().__init__()
        self.settings = setting
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
            'plot': False, 
            'generate-GIF': False,
            }
        self.project_id = project_id
        self.project_path = project_path
        self.data_path = data_path

        self.wrf_path = project_path / 'WRF/no_emission_run'
        self.pic_path = project_path / 'WRF/no_emission_run/pic'
        # self.gif_path = project_path / 'WRF/no_emission_run/gif'
        self.gif_path = pathlib.Path(
                self.settings.get("DUSTPATH_GIF_PATH")) / self.project_id

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
    
    def plot(self):
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

        ncfile = Dataset(
            pathlib.Path(
                f"{self.wrf_path}/wrfout_d01_2019-09-24_00:00:00"))

        cm = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', ['#00c7ff' , '#6ee44b', '#f1ff00', '#ffa500', '#ff0024'], 1024)
        days = np.arange(0,25)

        for i in days:
            PM2_5_DRY = getvar(ncfile, "PM2_5_DRY", timeidx=i)[0,:]
            DUST_1 = getvar(ncfile, "DUST_1", timeidx=i)[0,:]
            PM2_5 = DUST_1

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
            plt.title('PM2.5_DRY : ' + date)

            axs, _ = mpl.colorbar.make_axes(plt.gca(), shrink=0.5)  

            cbar = mpl.colorbar.ColorbarBase(axs, cmap=cm,
                            norm=mpl.colors.Normalize(vmin=-0, vmax=100))

            plt.savefig(
                pathlib.Path(f"{self.pic_path}") / pathlib.Path(str(i)+'.jpg'))
            # plt.show()
        self.status['plot'] = True
    
    def genarate_GIF_file(self):
        from PIL import Image, ImageDraw
        import numpy as np 

        image_frames=[]

        days = np.arange(0,25)

        for i in days:
            new_frame = Image.open(
                pathlib.Path(f"{self.pic_path}") / pathlib.Path(str(i)+'.jpg'))
            image_frames.append(new_frame)

        path = pathlib.Path(self.gif_path)
        if not path.exists() and not path.is_dir():
            path.mkdir(parents=True)

        image_frames[0].save(
            pathlib.Path(f"{path}/output.gif"), 
            format = 'GIF', append_images = image_frames[1: ], save_all = True, duration = 300, loop = 0) 

        # image_frames[0].save(
        #     pathlib.Path(f"{self.gif_path}/output.gif"), 
        #     format = 'GIF', append_images = image_frames[1: ], save_all = True, duration = 300, loop = 0) 
        self.status['generate-GIF'] = True

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
        if self.status['run-wrf']:
            logger.debug(f'plot')
            self.plot()
        if self.status['plot']:
        logger.debug(f'genarate_GIF_file')
        self.genarate_GIF_file()
        logger.debug("finish Wrf Runner And wait for get status")
        