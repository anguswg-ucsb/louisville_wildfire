# Angus Watters
# 01/26/2023
# Script for calculating wildfire risk raster using flame length, damage factors, and burn probability

# import external python libraries
import numpy as np
import rasterio as rio
import rioxarray as rxr
import pandas as pd
import geopandas as gpd
from rasterio.plot import show
import matplotlib.pyplot as plt
from os import scandir

# import utils functions py/utils.py
from py.utils import *

# path to shapefile to mask rasters
mask_path = "D:/louisville_wildfire/counties/aoi_counties.gpkg"

# path to burn probability raster
bp_path = "D:/louisville_wildfire/burn_prob/bp_clip_0514_tif/bp_clip_0514.tif"


# list of paths to Flame length rasters in order of lowest to highest flame length (0 -5)
r_paths = ["D:/louisville_wildfire/Flame_Length_Rasters/flp0/w001001.adf",
"D:/louisville_wildfire/Flame_Length_Rasters/flp1/w001001.adf",
"D:/louisville_wildfire/Flame_Length_Rasters/flp2/w001001.adf", 
"D:/louisville_wildfire/Flame_Length_Rasters/flp3/w001001.adf",
"D:/louisville_wildfire/Flame_Length_Rasters/flp4/w001001.adf",
"D:/louisville_wildfire/Flame_Length_Rasters/flp5/w001001.adf"]

# damage factor to apply to flame length rasters in order of lowest to highest flame length (0 - 5)
damage_factor = [0.0, 0.1, 0.25, 0.50, 0.75, 1.0]

# EPSG of output raster file
out_epsg      = 26913

# path to save final raster output too
out_path = "D:/louisville_wildfire/wildfire_risk/wildfire_risk.tif"


# call function to calculate and save out the wildfire risk raster calculations: 
#       Risk factor raster = (Burn Probability) * Σ(Flame Length(i) * damage_factor(i))
wildfire_risk = get_wildfire_risk(
    fl_paths      = r_paths,
    bp_path       = bp_path,
    mask_path     = mask_path,
    damage_factor = damage_factor,
    out_epsg      = out_epsg,
    save_path     = out_path
)