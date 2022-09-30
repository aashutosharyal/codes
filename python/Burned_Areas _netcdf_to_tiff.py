#MODIS Burned Areas for India study region
#09-16-2022

#Name format: YY_MM
#Uncertainty data could not be downloaded as TIF files

#python code used:
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import csv
import time

import os
from pathlib import Path
import glob
from datetime import datetime

#Define path to files
path = r'C:\Users\aashu\Downloads\India_Fire Project_UVA\raw_data'
files = sorted(glob.glob(path+"/*.nc"))
burn_date = xr.open_mfdataset(files,parallel=True,chunks={"lat": 100,"lon":100}).Burn_Date
burn_date_unc = xr.open_mfdataset(files,parallel=True,chunks={"lat": 100,"lon":100}).Burn_Date_Uncertainty
lat = burn_date.lat
lon = burn_date.lon

#Sum monthly burn days for each year
#burn_date_annual = burn_date.groupby("time.year").sum(dim="time")

#Spatial average of burn days per month
#burn_date_annual.mean(dim=['lat','lon']).plot()

date_index = enumerate(pd.date_range('01-01-2000','12-31-2021',freq='M'))
#To raster
for i in date_index:
    
    savename = datetime.strftime(i[1], '%y_%m')
    print(savename)

    new_array = xr.DataArray(burn_date[i[0]], dims=("lat", "lon"), coords={"lat": lat, "lon": lon}, name="burn_day")
    print(new_array)
    new_array.rio.set_crs("epsg:4326")
    new_array.rio.set_spatial_dims('lon','lat',inplace=True)
    new_array.rio.to_raster(r'C:\Users\aashu\Downloads\India_Fire Project_UVA\raw_data/{}.tif'.format(savename))

    #data format is in timedelta64 -- can't save as .tif file
  #  new_array = xr.DataArray(burn_date_unc[i[0]], dims=("lat", "lon"), coords={"lat": lat, "lon": lon}, name="burn_day_uncertainty")
   # print(new_array)
 #   new_array.rio.set_crs("epsg:4326")
 #   new_array.rio.set_spatial_dims('lon','lat',inplace=True)
 #   new_array.rio.to_raster(r'C:\Users\aashu\Downloads\India_Fire Project_UVA\raw_data\uncertainty/{}.tif'.format(savename))