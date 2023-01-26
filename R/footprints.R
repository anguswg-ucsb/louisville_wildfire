library(sf)
library(dplyr)
library(terra)
library(osmdata)
library(mapview)

# data directory path
dir_path <- "D:/louisville_wildfire"

# /aoi file paths
# aoi_paths <- list.files(file.path(dir_path, "aoi"), full.names = T)
#
# # Louisville AOI shp
# aoi <- sf::st_read(grep("shp", aoi_paths, value = T))
#
# mapview::mapview(aoi)
