import pathlib
from netCDF4 import Dataset
import matplotlib as mpl
import numpy as np
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                cartopy_ylim, latlon_coords)
import matplotlib.pyplot as plt
import cartopy.crs as crs

ncfile = Dataset(pathlib.Path("../../../wrf-build-script/container/projects/630708b2e560554e8fb05a9e/WRF/run/wrfout_d01_2019-09-21_00:00:00"))
cm = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', ['#00c7ff' , '#6ee44b', '#f1ff00', '#ffa500', '#ff0024'], 1024)
hours = np.arange(0, 24)

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

    path = pathlib.Path("../../../wrf-build-script/container/projects/630708b2e560554e8fb05a9e/WRF/run/pic")
    if not path.exists() and not path.is_dir():
        path.mkdir(parents=True)

    plt.savefig(
        pathlib.Path("../../../wrf-build-script/container/projects/630708b2e560554e8fb05a9e/WRF/run/pic") / pathlib.Path(str(i)+'.jpg'))

    plt.close(fig)