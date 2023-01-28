# Angus Watters
# Create fake fire data rasters to test python processing script out

library(raster)
library(terra)
library(climateR)
library(dplyr)

# *************************************
# ---- create fake firelength data ----
# *************************************

# r1 = terra::rast("D:/louisville_wildfire/Flame_Length_Rasters/flp0/w001001.adf")

tmp <- climateR::getTerraClim(
  AOI = AOI::aoi_get(state = "CA", county = "Santa Barbara"),
  param = climateR::param_meta$terraclim$common.name[4:9],
  startDate = "2018-01-09",
  endDate = "2018-01-09"
)


raster::writeRaster(tmp$terraclim_prcp, "D:/test_data/tif/single_layer_raster.tif")


shp <- AOI::aoi_get("UCSB") %>%
  sf::st_buffer(3500)

# mapview::mapview(shp)
tmp2 <- climateR::getTerraClim(
  AOI       = shp,
  param     = "prcp",
  startDate = "2018-01-09",
  endDate   = "2018-01-09"
)

out_dir <- "D:/test_data/tif/flame_length_rasters"

for (i in 1:6) {
  message(as.character(i-1))

  if(!dir.exists(out_dir)) {
    message(paste0("Creating top dir: ", out_dir))
    dir.create(out_dir)

    }


  r <- raster::setValues(
                        tmp2$terraclim_prcp,
                        ifelse(is.na(raster::values(tmp2$terraclim_prcp)), NA, i)
                      )

  if (!dir.exists(paste0(out_dir, "/flp", i - 1))) {
      message(paste0("Creating subdir: ", out_dir, "/flp", i - 1))

      dir.create(paste0(out_dir, "/flp", i - 1))
      paste0(out_dir, "/flp", i - 1, "/flp", i - 1, ".tif")
  }
  
  message(paste0("Saving ----> ", out_dir, "/flp", i-1, "/flp", i-1, ".tif"))

  r <- terra::rast(r)

  terra::writeRaster(
    r,
    paste0(out_dir, "/flp", i-1, "/flp", i-1, ".tif"),
    overwrite = TRUE
  )


}