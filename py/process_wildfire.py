# import packages
import numpy as np
import rasterio as rio
import rioxarray as rxr
import pandas as pd
import geopandas as gpd
from rasterio.plot import show
import matplotlib.pyplot as plt
from os import scandir

# path to shapefile to mask rasters
mask_path = "D:/louisville_wildfire/counties/aoi_counties.gpkg"

# directory 
fl_dir = "D:/test_data/tif/flame_length_rasters"

# 2nd level directories
fl_paths = [fl_dir + "/" + x + "/" + x + ".tif" for x in os.listdir(fl_dir)]
# dir_paths = [os.path.abspath(x).replace("\\","/") for x in os.listdir(fl_dir)]

# burn probability raster
bp_path = "D:/louisville_wildfire/burn_prob/bp_clip_0514_tif/bp_clip_0514.tif"

# r_paths = ["D:/louisville_wildfire/Flame_Length_Rasters/flp0/w001001.adf",
# "D:/louisville_wildfire/Flame_Length_Rasters/flp1/w001001.adf",
# "D:/louisville_wildfire/Flame_Length_Rasters/flp2/w001001.adf", 
# "D:/louisville_wildfire/Flame_Length_Rasters/flp3/w001001.adf",
# "D:/louisville_wildfire/Flame_Length_Rasters/flp4/w001001.adf", 
# "D:/louisville_wildfire/Flame_Length_Rasters/flp5/w001001.adf"]
