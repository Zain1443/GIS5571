import arcpy
from arcpy import env
import pandas as pd
import requests
import os
import io
import sys

#All Input Shapefiles into Geodatabase
arcpy.conversion.FeatureClassToGeodatabase(r"'E:\GIS\ArcGIS Layers\1. All Layers\Roads\roads\Roads.shp';'E:\GIS\ArcGIS Layers\1. All Layers\Sindh\Sindh.shp';'E:\GIS\ArcGIS Layers\1. All Layers\Surface Water\Final\Wat_lay_final\Surface Water.shp';'E:\GIS\ArcGIS Layers\1. All Layers\Cities\Major Cities.shp';'E:\GIS\ArcGIS Layers\Thesis (Mapping)\CCPP_in_Sindh.shp';'E:\GIS\ArcGIS Layers\Thesis (Mapping)\RLNG.shp';'E:\GIS\ArcGIS Layers\Thesis (Mapping)\Electric Transmission Lines.gdb\Placemarks\PowerTransmissionLines';'E:\GIS\ArcGIS Layers\Pakistan\pak_admbnda_adm0_wfp_20220909.shp'", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb")

#DEM
env.workspace = r"E:\GIS\ArcGIS Layers\1. All Layers\DEM"

arcpy.conversion.RasterToGeodatabase("DEM.tif", 
                                     "CCPPArcGIS-FinalProject.gdb")

#Vegetation
env.workspace = r"E:\GIS\ArcGIS Layers\1. All Layers\Initial Criteria Layers\Selection Criteria"

arcpy.conversion.RasterToGeodatabase("vegetation.tif", 
                                     "CCPPArcGIS-FinalProject.gdb")

#Slope
with arcpy.EnvManager(mask="Sindh"):
    Slope = arcpy.sa.Slope("DEM", "DEGREE", 1, "PLANAR", "METER"); Slope.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\Slope")



#Gas Pipeline
with arcpy.EnvManager(XYDomain="-400 -400 8099972.86318398 8099972.86318398", extent='66.6544306134821 23.6892920246073 71.1263735409062 28.5012823071328 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],VERTCS["EGM96_Geoid",VDATUM["EGM96_Geoid"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]]', outputMFlag="Enabled"):
    arcpy.analysis.MultipleRingBuffer("RLNG", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\RLNG_MultipleRingBuffer", [5,20,50,100,300], "Kilometers", "distance", "ALL", "FULL", "GEODESIC")
    
#Masking
arcpy.analysis.Clip("RLNG_MultipleRingBuffer", "Sindh", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\RLNG_Clip", None)

#Power Grid
with arcpy.EnvManager(extent='66.6544306134821 23.6892920246073 71.1263735409062 28.5012823071328 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],VERTCS["EGM96_Geoid",VDATUM["EGM96_Geoid"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]]'):
    arcpy.analysis.MultipleRingBuffer("PowerTransmissionLines", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\PTL_MultipleRingBuffer", [3,12,36,72,165], "Kilometers", "distance", "ALL", "FULL", "GEODESIC")
    
#Masking
arcpy.analysis.Clip("PTL_MultipleRingBuffer", "Sindh", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\PTL_Clip", None)

#Major Cities
with arcpy.EnvManager(extent='66.6544306134821 23.6892920246073 71.1263735409062 28.5012823071328 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],VERTCS["EGM96_Geoid",VDATUM["EGM96_Geoid"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]]'):
    arcpy.analysis.MultipleRingBuffer("Major_Cities", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\Major_Cities_MultipleRingBuffer", [5,15,45,90,150], "Kilometers", "distance", "ALL", "FULL", "GEODESIC")
    
#Masking
arcpy.analysis.Clip("Major_Cities_MultipleRingBuffer", "Sindh", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\MajorCities_Clip", None)

#Streams
with arcpy.EnvManager(extent='66.6544306134821 23.6892920246073 71.1263735409062 28.5012823071328 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],VERTCS["EGM96_Geoid",VDATUM["EGM96_Geoid"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]]'):
    arcpy.analysis.MultipleRingBuffer("Surface Water", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\SurfaceWater_MultipleRingBuffer", [3,10,30,60,150], "Kilometers", "distance", "ALL", "FULL", "PLANAR")

#Masking
arcpy.analysis.Clip("SurfaceWater_MultipleRingBuffer", "Sindh", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\SurfaceWater_Clip", None)

#Roads
with arcpy.EnvManager(XYDomain="-400 -400 8099972.86318398 8099972.86318398"):
    arcpy.analysis.MultipleRingBuffer("Roads", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\Roads_MultipleRingBuffer", [3,10,30,60,150], "Kilometers", "distance", "ALL", "FULL", "GEODESIC")
    
#Masking
arcpy.analysis.Clip("Roads_MultipleRingBuffer", "Sindh", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\Roads_Clip", None)





#Gas Pipeline
arcpy.conversion.FeatureToRaster("RLNG_Clip", "distance", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\RLNG_Raster", 0.0178877717096966)

#Power Grid
arcpy.conversion.FeatureToRaster("PTL_Clip", "distance", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\PTL_Raster", 0.0178877717120001)

#Major Cities
arcpy.conversion.FeatureToRaster("MajorCities_Clip", "distance", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\MajorCities_Raster", 0.0178877717096966)

#Streams
arcpy.conversion.FeatureToRaster("SurfaceWater_Clip", "distance", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\SurfaceWater_Raster", 1810.57403204286)

#Roads
arcpy.conversion.FeatureToRaster("Roads_Clip", "distance", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\Roads_Raster", 0.0178877717096966)

#Gas Pipeline
with arcpy.EnvManager(mask="Sindh"):
    RLNG_Reclass = arcpy.sa.Reclassify("RLNG_Raster", "Value", "5 9;20 7;50 5;100 3;300 1;NODATA 1", "DATA"); RLNG_Reclass.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\RLNG_Reclass")

#Power Grid
with arcpy.EnvManager(mask="Sindh"):
    PTL_Reclass = arcpy.sa.Reclassify("PTL_Raster", "Value", "3 9;12 7;36 5;72 3;165 1;NODATA 1", "DATA"); PTL_Reclass.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\PTL_Reclass")

#Major Cities
with arcpy.EnvManager(mask="Sindh"):
    MajorCities_Reclass = arcpy.sa.Reclassify("MajorCities_Raster", "Value", "5 1;15 3;45 5;90 7;150 9;NODATA 9", "DATA"); MajorCities_Reclass.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\MajorCities_Reclass")

#Streams
with arcpy.EnvManager(mask="Sindh"):
    Strams_Reclass = arcpy.sa.Reclassify("SurfaceWater_Raster", "Value", "3 9;10 7;30 5;60 3;150 1;NODATA 1", "DATA"); Strams_Reclass.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\SurfaceWater_Reclass")

#Roads
with arcpy.EnvManager(mask="Sindh"):
    Roads_Reclass = arcpy.sa.Reclassify("Roads_Raster", "Value", "3 9;10 7;30 5;60 3;150 1;NODATA 1", "DATA"); Roads_Reclass.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\Roads_Reclass")

#Vegetation
with arcpy.EnvManager(mask="Sindh"):
    Vegetation_Reclass = arcpy.sa.Reclassify("Vegetation", "Value", "1 9;2 1;NODATA 1", "DATA"); Vegetation_Reclass.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\Vegetation_Reclass")

#DEM
with arcpy.EnvManager(mask="Sindh"):
    DEM_Reclass = arcpy.sa.Reclassify("DEM", "Value", "-187 15 1;16 50 9;51 100 7;101 200 5;201 500 3;501 2152 1;NODATA 1", "DATA"); DEM_Reclass.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\DEM_Reclass")

#Slope
with arcpy.EnvManager(mask="Sindh"):
    Slope_Reclass = arcpy.sa.Reclassify("Slope", "VALUE", "0 1.500000 9;1.500000 3 7;3 6 5;6 12 3;12 76.465958 1;NODATA 1", "DATA"); Slope_Reclass.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\Slope_Reclass")

# Weighted Overlay (As per AHP Weights)
WeightedOverlay = arcpy.sa.WeightedOverlay(r"('C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\RLNG_Reclass' 27 'Value' (1 1; 3 3; 5 5; 7 7; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\PTL_Reclass' 15 'Value' (1 1; 3 3; 5 5; 7 7; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\MajorCities_Reclass' 15 'Value' (1 1; 3 3; 5 5; 7 7; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\SurfaceWater_Reclass' 10 'Value' (1 1; 3 3; 5 5; 7 7; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\Roads_Reclass' 12 'Value' (1 1; 3 3; 5 5; 7 7; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\Vegetation_Reclass' 10 'Value' (1 1; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\DEM_Reclass' 7 'Value' (1 1; 3 3; 5 5; 7 7; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\Slope_Reclass' 4 'Value' (1 1; 3 3; 5 5; 7 7; 9 9; NODATA NODATA));1 9 1"); WeightedOverlay.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\Weighte_RLNG1")

# Weighted Sum (As per AHP Weights)
WeightedSum = arcpy.sa.WeightedSum("RLNG_Reclass Value 0.2737;PTL_Reclass Value 0.1538;MajorCities_Reclass Value 0.1528;SurfaceWater_Reclass Value 0.0982;Roads_Reclass Value 0.1139;Vegetation_Reclass Value 0.0992;DEM_Reclass Value 0.0674;Slope_Reclass Value 0.0414"); WeightedSum.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\WeightedSum")

# Weighted Sum 
#Scenario 1
#Gas 10; Power Grid 10; City Distance 10; Distance from Water Source 15; Roads 10; Vegetation 15; Elevation 15; Slope 15. 
WS1 = arcpy.sa.WeightedSum("RLNG_Reclass Value 0.10;PTL_Reclass Value 0.10;MajorCities_Reclass Value 0.10;SurfaceWater_Reclass Value 0.15;Roads_Reclass Value 0.10;Vegetation_Reclass Value 0.15;DEM_Reclass Value 0.15;Slope_Reclass Value 0.15"); WS1.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\WeightedSum")

#Scenario 2
#Gas 5; Power Grid 5; City Distance 15; Distance from Water Source 15; Roads 10; Vegetation 15; Elevation 20; Slope 15. 
WS2 = arcpy.sa.WeightedSum("RLNG_Reclass Value 0.05;PTL_Reclass Value 0.05;MajorCities_Reclass Value 0.15;SurfaceWater_Reclass Value 0.15;Roads_Reclass Value 0.10;Vegetation_Reclass Value 0.15;DEM_Reclass Value 0.20;Slope_Reclass Value 0.15"); WS2.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\WeightedSum")

#Scenario 3
#Gas 3; Power Grid 2; City Distance 25; Distance from Water Source 20; Roads 15; Vegetation 10; Elevation 5; Slope 20. 
WS3 = arcpy.sa.WeightedSum("RLNG_Reclass Value 0.03;PTL_Reclass Value 0.02;MajorCities_Reclass Value 0.25;SurfaceWater_Reclass Value 0.20;Roads_Reclass Value 0.15;Vegetation_Reclass Value 0.10;DEM_Reclass Value 0.05;Slope_Reclass Value 0.20"); WS1.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\WeightedSum")

#Weighted Overlay
arcpy.sa.ZonalStatisticsAsTable("GenerateTessellationWO", "GRID_ID", "WeightedOverlay", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\ZonalSt_WO", "DATA", "MEAN", "CURRENT_SLICE", 90, "AUTO_DETECT", "ARITHMETIC", 360)

#Zonal Statistics as Table
arcpy.sa.ZonalStatisticsAsTable("GenerateTessellationWO", "GRID_ID", "WeightedOverlay", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\ZonalSt_WO", "DATA", "MEAN", "CURRENT_SLICE", 90, "AUTO_DETECT", "ARITHMETIC", 360)

#Weighted Sum
arcpy.management.GenerateTessellation(r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\GenerateTessellationWS", '66.6544306134821 23.6892920246073 71.0905979980581 28.5011026151353 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],VERTCS["EGM96_Geoid",VDATUM["EGM96_Geoid"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]]', "HEXAGON", "10 SquareKilometers", 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],VERTCS["EGM96_Geoid",VDATUM["EGM96_Geoid"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')

#Zonal Statistics as Table 
arcpy.ia.ZonalStatisticsAsTable("GenerateTessellationWS", "GRID_ID", "WeightedSum", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\ZonalSt_WeightedSum", "DATA", "MEAN", "CURRENT_SLICE", 90, "AUTO_DETECT", "ARITHMETIC", 360)

#Weighted Sum
arcpy.stats.OptimizedHotSpotAnalysis("GenerateTessellationWS", r"C:\Users\siyal\Documents\ArcGIS\Projects\CCPPArcGIS-FinalProject\CCPPArcGIS-FinalProject.gdb\GenerateTessellationWS_OptimizedHotSpotAnalysis", "ZonalSt_WeightedSum.MEAN", "COUNT_INCIDENTS_WITHIN_FISHNET_POLYGONS", None, None, None, None, None)
