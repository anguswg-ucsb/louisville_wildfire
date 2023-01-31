# louisville_wildfire
City of Louisville Wildfire project code repository

## **Generating wildfire risk raster**
The `py/utils.py` script in this repository contains a **`get_wildfire_risk()`** function that will take a set of specific arguments and return a wildfire risk raster according to the following formula:

##### **Risk factor raster = (Burn Probability) * Σ(Flame Length(i) * damage_factor(i))**

## **Inputs:**
The **`get_wildfire_risk()`** function requires 5 key arguments and an optional 6th argument to save the output:

1. `fl_path`: A list of paths to flame length rasters in order of lowest to highest flame length category (0 -5)
2. `bp_path`: Path to burn probability raster
3. `mask_path`: Path to a shapefile to mask rasters to
4. `damage_factor`: List of damage factors to apply to flame length rasters provided in order smallest to highest flame length category (0 -5)
5. `out_epsg`: EPSG code that will be assigned to the output raster
6. `save_path`: Optional, a file path to save the output raster too. Defaults to None and output raster will not be saved. 

## **Spatial mask:**
The `/data` directory contains a **.gpk** file of Broomfield, Weld, and Boulder county polygons that can be used to mask the raster data (mask_path).

![](https://louisville-wildfire.s3.us-west-1.amazonaws.com/plots/county_plot.png)

## **Example inputs:**
Below is an example template of valid inputs to **`get_wildfire_risk()`**
```python

# list of paths to Flame length rasters in order of lowest to highest flame length (0 -5)
fl_paths = ["D:/louisville_wildfire/Flame_Length_Rasters/flp0/w001001.adf",
"D:/louisville_wildfire/Flame_Length_Rasters/flp1/w001001.adf",
"D:/louisville_wildfire/Flame_Length_Rasters/flp2/w001001.adf", 
"D:/louisville_wildfire/Flame_Length_Rasters/flp3/w001001.adf",
"D:/louisville_wildfire/Flame_Length_Rasters/flp4/w001001.adf",
"D:/louisville_wildfire/Flame_Length_Rasters/flp5/w001001.adf"]

# path to burn probability raster
bp_path       = "D:/louisville_wildfire/burn_prob/bp_clip_0514_tif/bp_clip_0514.tif"

# path to shapefile to mask rasters
mask_path     = "data/aoi_counties.gpkg"

# damage factor to apply to flame length rasters in order of lowest to highest flame length (0 - 5)
damage_factor = [0.0, 0.1, 0.25, 0.50, 0.75, 1.0]

# EPSG of output raster file
out_epsg      = 26913

# path and filename to save final raster output too
out_path      = "D:/louisville_wildfire/wildfire_risk/wildfire_risk.tif"
```

<br>

## **Calculating wildfire risk raster:**
Given these inputs, we can calculate a wildfire risk raster like so:

```python

# call get_wildfire_risk and 
wildfire_risk = get_wildfire_risk(
    fl_paths      = fl_paths,
    bp_path       = bp_path,
    mask_path     = mask_path,
    damage_factor = damage_factor,
    out_epsg      = out_epsg,
    save_path     = out_path            # save raster to given save_path
)
```

![](https://louisville-wildfire.s3.us-west-1.amazonaws.com/plots/wildfire_risk_plot.png)