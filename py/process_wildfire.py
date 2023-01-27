import numpy as np
import rasterio as rio
from rasterio.plot import show
import rioxarray as rxr
import matplotlib.pyplot as plt
import geopandas as gpd
import os
import os.path
import pandas as pd

# path to ADF files where each flame length is within a folder
fl_path = "D:/louisville_wildfire/Flame_Length_Rasters"

files_path = [os.path.abspath(x) for x in os.listdir(fl_path)]

# path to shapefile to mask rasters
mask_path = "D:/louisville_wildfire/counties/aoi_counties.gpkg"

# read in mask shapefile w/ geopandas
counties  = gpd.read_file(mask_path)

# def parse_dir(directory,urls=None):
# 		filenames = []
# 		for filename in os.scandir(directory):
# 			filenames.append(filename.path)
# 		return filenames

# fl_dirs = [x.replace("\\", "/") for x in parse_dir(directory = fl_path)]

# fl_files = [x.replace("\\", "/") for x in parse_dir(directory = fl_dirs)]
# with os.scandir(fl_path) as i:
#     for entry in i:
#         if entry.is_file():
#             print(entry.name)
# parse_dir(directory = fl_dirs[1])
# [os.path.abspath(f) for f in os.scandir(fl_dirs[1]) if f.is_file()]
# x.replace("//", "\\")
# for txt in fl_dirs:
#     # replace() "returns" an altered string
#     string = string.replace(txt, "//")

# type(fl_dirs)

# os.listdir("D:/louisville_wildfire/Flame_Length_Rasters")

# files_path = [os.path.abspath(x) for x in os.listdir(fl_path)]
# print(files_path)
# [f for f in os.listdir(fl_path) if os.path.isfile(os.path.join(fl_path, f))]
# import os
# x = [f.name for f in os.scandir() if f.is_file()]
# # from os import listdir
# # from os.path import isfile, join
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# [f for f in listdir(fl_path) if isfile(join(fl_path, f))]
# path to flame length raster

r_paths = ["D:/louisville_wildfire/Flame_Length_Rasters/flp0/w001001.adf",
"D:/louisville_wildfire/Flame_Length_Rasters/flp1/w001001.adf",
"D:/louisville_wildfire/Flame_Length_Rasters/flp2/w001001.adf", 
"D:/louisville_wildfire/Flame_Length_Rasters/flp3/w001001.adf",
"D:/louisville_wildfire/Flame_Length_Rasters/flp4/w001001.adf", 
"D:/louisville_wildfire/Flame_Length_Rasters/flp5/w001001.adf"]

def damage_index():
    damage_df = pd.DataFrame({
        'flame_length' : ["fl0", "fl1", "fl2", "fl3", "fl4", "fl5"], 
        'damage' : [0.0, 0.25, 0.50, 0.75, 1.0, 1.0]
        })
    return damage_df

damage_index()

damages = damage_index()
for idx, val in enumerate(r_paths):
    # print(idx, "-", val)
    print(damages.flame_length[idx], "-", damages.damage[idx])
    # damages.damage[0]flame_length
    # damages = damage_index()

def calc_wildfire_risk(
        fl_paths   = None, 
        bp_paths   = None,
        mask_path  = None  
        ): 
    # read in mask shapefile w/ geopandas
    counties  = gpd.read_file(mask_path)
    
    damages = damage_index()

    for idx, val in enumerate(fl_paths):
        print(idx, "-", val)
    
        # read in flame length raster
        r1       = rxr.open_rasterio(fl_paths, masked = True).squeeze()

        # reproject raster and shapefile to match (EPSG:26913)
        r1       = r1.rio.reproject(26913)
        counties = counties.to_crs(26913) 

        # clip flamelength rasters to county shapefile
        r1       = r1.rio.clip(counties.geometry.values, counties.crs)

        r1 = r1*damages.damage[idx]

        




# r_path = "D:/test_data/tif/single_layer_raster2.tif"

r1 = rxr.open_rasterio("D:/test_data/tif/single_layer_raster2.tif", masked = True).squeeze()
sum([r1, r1])
r1.rio + r1.rio
r1*0.5
type(r1 + r1)
# read in flame length raster
r1 = rxr.open_rasterio(r_path, masked = True).squeeze()

# reproject raster and shapefile to match (EPSG:26913)
r1       = r1.rio.reproject(26913)
counties = counties.to_crs(26913) 

# clip flamelength rasters to county shapefile
r1 = r1.rio.clip(counties.geometry.values, counties.crs)


clipped.rio.crs
# When you try to overlay the building footprints the data don't line up
f, ax = plt.subplots()
clipped.plot.imshow(ax=ax, cmap='Greys')

plt.show()

r2 = r1.rio.reproject(26913)

type(r2)
r2.rio.crs
show(r2)
# shape of raster
r1.shape

# plot raster bands
show(r1)

# number of rows and columns
nrows = r1.height
ncols = r1.width

# read raster as numpy array
arr = r1.read(1)
arr
arr = np.around(arr, decimals = 3)
arr[arr == -np.inf] = None
arr/arr

arr*arr 

arr.plot()
with rasterio.open('source/_static/data/L5/forest_loss_porijogi_wgs84.tif') as src:transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds)
kwargs = src.meta.copy()
kwargs.update({ 
    'crs': dst_crs,
    'transform': transform,
    'width': width,
    'height': height
    })
with rasterio.open('source/_static/data/L5/forest_loss_porijogi_3301.tif', 'w', **kwargs) as dst:
    for i in range(1, src.count + 1):
        reproject(
            source=rasterio.band(src, i),
            destination=rasterio.band(dst, i),
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=transform,
            dst_crs=dst_crs,
            resampling=Resampling.nearest
            )
arr
total = np.zeros(r1.shape)
-np.inf
for band in r, g, b:
    total += band
type(r1)
with rasterio.open('tests/data/RGB.byte.tif') as src:
    r, g, b = src.read()

# Combine arrays in place. Expecting that the sum will
# temporarily exceed the 8-bit integer range, initialize it as
# a 64-bit float (the numpy default) array. Adding other
# arrays to it in-place converts those arrays "up" and
# preserves the type of the total array.
total = np.zeros(r.shape)

for band in r, g, b:
    total += band

total /= 3
plot(r1)
r1.plot()