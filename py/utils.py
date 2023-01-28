# import packages
import numpy as np
import rasterio as rio
import rioxarray as rxr
import pandas as pd
import geopandas as gpd
from rasterio.plot import show
import matplotlib.pyplot as plt
from os import scandir

def parse_dir(directory,urls = None):
		filenames = []
		for filename in os.scandir(directory):
			filenames.append(filename.path)
		return filenames

def damage_index(
            factor = None
            ):

    # if no factor is specified, set all to 1
    if factor is None:
        factor = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    damage_df = pd.DataFrame({
        'flame_length' : ["fl0", "fl1", "fl2", "fl3", "fl4", "fl5"], 
        'damage' : factor
        })
    
    return damage_df

def get_wildfire_risk(
        fl_paths      = None, 
        bp_path       = None,
        mask_path     = None,
        damage_factor = None,
        out_epsg      = None,
        save_path     = None
        ):
    """Create wildfire risk raster using flame length and burn probability rasters 

    Takes the flame length rasters, damage factors, and a burn probability raster and performs the following risk calculations:
    
    Risk factor raster = (Burn Probability) * Σ(Flame Length(i) * damage_factor(i))

    Args:
        fl_paths (list): List of paths to flame length rasters.
        List must be of length 6 and provided in order of lowest to highest flame length category (0 to 5). Defaults to None.
        bp_path (str): Path to burn probability raster. Defaults to None.
        mask_path (str): Path to a shapefile to mask rasters to. Defaults to None.
        damage_factor (list, optional): List of damage factors to apply to flame length rasters provided in order smallest to highest flame length category (0 -5).
        Defaults to None, which will result in damage factors of 1.0 for all flame length rasters (flame length * 1.0).
        out_epsg (int, str, float): EPSG code that will be assigned to the output raster. Defaults to None.
        save_path (str, optional): Optional, a file path to save the output raster too. Defaults to None and output raster will not be saved. 

    Returns:
        rioxarray: single banded raster clipped to the mask area
    """

    if out_epsg is None:
        raise ValueError("Invalid 'out_epsg' argument, provide an EPSG integer code specifying the desired EPSG of the output raster")

    # check if out_epsg is a string or float and converts to integer 
    if(isinstance(out_epsg, str, float)):
        out_epsg = int(out_epsg)

    # read in mask shapefile w/ geopandas
    shp     = gpd.read_file(mask_path)
    
    # damage  factor data frame 
    damages = damage_index(factor = damage_factor)

    # empty list
    r_lst = []

    print("Applying damage factors to flame length rasters")

    # loop through paths to flame length rasters in order of lowest to highest flame length rasters (0 - 5)
    for idx, val in enumerate(fl_paths):

        print(str(idx)+"/" + str(len(fl_paths)))

        # read in flame length raster
        r1       = rxr.open_rasterio(val, masked = True).squeeze()

        # reproject raster and shapefile to match (EPSG:26913)
        r1       = r1.rio.reproject(out_epsg)

        # clip flame length rasters to county shapefile
        r1       = r1.rio.clip(shp.to_crs(out_epsg).geometry.values, shp.to_crs(out_epsg).crs)

        # multiply flamelength raster values by damage factor values
        r1       = r1*damages.damage[idx]

        r_lst.append(r1)

    # total flame length rasters after damage factors
    total_fl  = sum(r_lst)

    # read in burn probability raster
    bp        = rxr.open_rasterio(bp_path, masked = True).squeeze()

    print("Clipping burn probability raster to shape geometry")

    # using provided burn probability raster CRS, transform mask shape to that CRS,
    # and clip/mask the burn probability raster to the transformed geometry 
    bp        = bp.rio.clip(shp.to_crs(bp.rio.crs).geometry.values, shp.to_crs(bp.rio.crs).crs)

    # reproject burn probability raster to out_epsg code 
    bp        = bp.rio.reproject(out_epsg)
    
    # reproject/resample burn probability to align with total flame length raster 
    bp        = bp.rio.reproject_match(total_fl)

    # calculate final Wildfire risk raster by:
    # Burn probability + sum(Flame lengths * risk factors) 
    risk_rast = bp + total_fl

    # save out raster if a save path is provided
    if save_path is not None:

        print("Saving final raster to:\n" + save_path)

        risk_rast.rio.to_raster(
            raster_path = save_path, 
            tiled       = True,  # force creates tiled TIF files
            windowed    = True
            )
        
    return risk_rast


# path to ADF files where each flame length is within a folder
# fl_path = "D:/louisville_wildfire/Flame_Length_Rasters"
# files_path = [os.path.abspath(x) for x in os.listdir(fl_path)]
# fl_dirs = [x.replace("\\", "/") for x in parse_dir(directory = fl_path)]
# fl_files = [x.replace("\\", "/") for x in parse_dir(directory = fl_dirs)]
# files_path = [os.path.abspath(x) for x in os.listdir(fl_path)]
# [f for f in os.listdir(fl_path) if os.path.isfile(os.path.join(fl_path, f))]
# x = [f.name for f in os.scandir() if f.is_file()]
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# [f for f in listdir(dir_paths) if isfile(join(dir_paths, f))]
# # file_names = ["/" + x + ".tif" for x in os.listdir(fl_dir)]
# # list of flame length paths
# # fl_paths = [dir_paths[x] + file_names[x] for x in range(len(dir_paths))]