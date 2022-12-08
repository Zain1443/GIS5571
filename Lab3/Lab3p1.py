import arcpy
import requests
import os
import zipfile
import io
import sys

#Dory Starting & Ending Points
arcpy.management.XYTableToPoint(r"C:\Users\siyal\Desktop\1. UMN MGIS\1. Semesters\1st Semester\2. ArcGIS I\1. Labs\Lab 3\Starting & End Points\StartingEndingPoints.csv", r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\StartingEndingPoints", "Long", "Lat", None, 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')

#Dory Starting Point
arcpy.management.XYTableToPoint(r"C:\Users\siyal\Desktop\1. UMN MGIS\1. Semesters\1st Semester\2. ArcGIS I\1. Labs\Lab 3\Starting & End Points\Dory Starting Point.csv", r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\DoryStartingPoint", "Long", "Lat", None, 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')

#Dory Destination Point
arcpy.management.XYTableToPoint(r"C:\Users\siyal\Desktop\1. UMN MGIS\1. Semesters\1st Semester\2. ArcGIS I\1. Labs\Lab 3\Starting & End Points\DestinationPoint.csv", r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\DoryDestinationPoint", "Long", "Lat", None, 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')

#Streams Layer
#Reclassify the layer by assigning preferences (1-Highest ; 9-Lowest)
with arcpy.EnvManager(mask="mn_county_boundarie_Dissolve2"):
    Reclass_Streams = arcpy.sa.Reclassify("Streams Raster Layer", "Value", "0 13757 1;13757 27514 2;27514 41271 3;41271 55028 4;55028 68785 5;68785 82542 6;82542 96299 7;96299 110056 8;110056 123813 9;NODATA 9", "DATA"); Reclass_Streams.save(r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Reclass_Streams")

#DEM Data
#Slope Extraction
with arcpy.EnvManager(mask="mn_county_boundarie_Dissolve2"):
    Slope = arcpy.sa.Slope("DEM_Study_Extent", "PERCENT_RISE", 1, "PLANAR", "METER"); Slope.save(r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Slope")
#Reclassify the data by assigning preferences (1-Highest ; 9-Lowest)
with arcpy.EnvManager(mask="mn_county_boundarie_Dissolve2"):
    Reclass_Slope = arcpy.sa.Reclassify("Slope", "VALUE", "0 3 1;3 6 2;6 10 3;10 15 4;15 20 5;20 25 6;25 30 7;30 40 8;40 1000 9;NODATA 9", "DATA"); Reclass_Slope.save(r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Reclass_Slope")

#Road Data
#Reclassify the data by assigning preferences (9-Highest ; 1-Lowest)
with arcpy.EnvManager(mask="mn_county_boundarie_Dissolve2"):
    Reclass_Roads = arcpy.sa.Reclassify("Roads_Study_Extent", "Value", "0 0.000001 9;0.000001 5 7;5 30 5;30 60 3;60 100 1;NODATA 5", "DATA"); Reclass_Roads.save(r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Reclass_Roads")

#Land Cover
#Reclassify the data by assigning preferences
with arcpy.EnvManager(mask="mn_county_boundarie_Dissolve2"):
    Reclass_LULC = arcpy.sa.Reclassify("Land_Cover", "NLCD_Land", "'Open Water' 9;'Developed, Open Space' 1;'Developed, Low Intensity' 2;'Developed, Medium Intensity' 3;'Developed, High Intensity' 4;'Barren Land' 1;'Deciduous Forest' 7;'Evergreen Forest' 8;'Mixed Forest' 7;Shrub/Scrub 5;Herbaceous 6;Hay/Pasture 6;'Cultivated Crops' 5;'Woody Wetlands' 7;'Emergent Herbaceous Wetlands' 8;NODATA 5", "DATA"); Reclass_LULC.save(r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Reclass_LULC")

#Weighted Overlay
#Input Weights: Streams=5; LULC=10; Slope=73; Roads=12
WeightedOverlay1 = arcpy.sa.WeightedOverlay(r"('C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Reclass_LULC' 10 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; 6 6; 7 7; 8 8; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Reclass_Streams' 5 'Value' (1 1; 8 8; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Reclass_Slope' 73 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; 6 6; 7 7; 8 8; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Reclass_Roads' 12 'Value' (1 1; 3 3; 5 5; 7 7; 9 9; NODATA NODATA));1 9 1"); WeightedOverlay1.save(r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\WeightedOverlay1")

#Input Weights: Streams=1; LULC=3; Slope=95; Roads=1
WeightedOverlay2 = arcpy.sa.WeightedOverlay(r"('C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Reclass_LULC' 3 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; 6 6; 7 7; 8 8; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Reclass_Streams' 1 'Value' (1 1; 8 8; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Reclass_Slope' 95 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; 6 6; 7 7; 8 8; 9 9; NODATA NODATA); 'C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\Reclass_Roads' 1 'Value' (1 1; 3 3; 5 5; 7 7; 9 9; NODATA NODATA));1 9 1"); WeightedOverlay2.save(r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\WeightedOverlay2")

#Weighted Sum
#Input Weights: Streams=80; LULC=5; Slope=7; Roads=8
WeightedSum = arcpy.sa.WeightedSum("Reclass_Streams Value 0.8;Reclass_Roads Value 0.08;Reclass_Slope Value 0.07;Reclass_LULC Value 0.05"); WeightedSum.save(r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\WeightedSum")

# Path 01 (Using Optimal Regional Conection)
arcpy.sa.OptimalRegionConnections("StartingEndingPoints", r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\OP1", None, "WeightedOverlay1", None, "PLANAR", "GENERATE_CONNECTIONS")

# Path 02 (Using Optimal Regional Conection)
arcpy.sa.OptimalRegionConnections("StartingEndingPoints", r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\OP2", None, "WeightedOverlay2", None, "PLANAR", "GENERATE_CONNECTIONS")

# Path 03 (Using Optimal Regional Conection)
arcpy.sa.OptimalRegionConnections("StartingEndingPoints", r"C:\Users\siyal\Documents\ArcGIS\Dora_ArcGIS_Lab02\MyProject3\MyProject3.gdb\OP3", None, "WeightedSum", None, "PLANAR", "GENERATE_CONNECTIONS")
