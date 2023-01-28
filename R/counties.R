library(sf)
library(AOI)
library(mapview)
library(dplyr)

# county shapefiles
broomfield <- AOI::aoi_get(state = "CO", county = "Broomfield")
weld       <- AOI::aoi_get(state = "CO", county = "Weld")
boulder    <- AOI::aoi_get(state = "CO", county = "Boulder")

# Join counties to single sf object
counties <-
    dplyr::bind_rows(broomfield, weld, boulder) %>%
    dplyr::select(county = name, geometry) %>%
    sf::st_transform(26913)

# save out county shape as geopackage
sf::write_sf(counties, "D:/louisville_wildfire/counties/aoi_counties.gpkg")
