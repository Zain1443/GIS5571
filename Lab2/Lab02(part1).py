import arcpy
import requests
import os
import zipfile
import io
import sys

working_dir = r'C:\Users\siyal\Desktop\Lab 02'

mn_geo = r'https://resources.gisdata.mn.gov/pub'

'https://resources.gisdata.mn.gov/pub'

las_file=r'https://resources.gisdata.mn.gov/pub/data/elevation/lidar/examples/lidar_sample/las/4342-12-05.las'
las_file

las_file_obj = requests.post(las_file)

las_file_obj

path_to_las = os.path.join(working_dir, 'output.las')
path_to_las

with open(path_to_las, 'wb') as f:
    f.write(las_file_obj.content)

arcpy.conversion.LasDatasetToRaster(r"C:\Users\siyal\Desktop\Lab 02\output.las", r"c:\users\siyal\documents\arcgis\projects\arcgis (lab 02)\arcgis (lab 02).gdb\output_lasda", "ELEVATION", "BINNING AVERAGE LINEAR", "FLOAT", "CELLSIZE", 10, 1)

arcpy.ddd.LasDatasetToTin(r"C:\Users\siyal\Desktop\Lab_02\output.las", r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS (Lab 02)\output_LasDatasetToTIN", "RANDOM", "PERCENT", 75, 5000000, 1, "CLIP")

####arcpy.management.SaveToLayerFile(in_layer, out_layer)####

aprx = arcpy.mp.ArcGISProject("CURRENT")

aprx.defaultGeodatabase = (r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS (Lab 02)\ArcGIS (Lab 02).gdb")

print(aprx.filepath)

aprx = arcpy.mp.ArcGISProject(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS (Lab 02)\ArcGIS (Lab 02).aprx")

arcpy.server.GetLayoutTemplatesInfo(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS (Lab 02)")

lyt = aprx.listLayouts('Layout')[0]

lyt.exportToPDF(r"C:\Users\siyal\Desktop\Lab 02.pdf", resolution = 300)

lyt = aprx.listLayouts('Layout1')[0]

Outputpath= (r"C:\Users\siyal\Desktop\Lab_02\Tin.pdf")
Outputpath

lyt.exportToPDF(r'C:\Users\siyal\Desktop\Lab_02\Tin.pdf", resolution = 300)



PRISM_request_URL = r'https://prism.oregonstate.edu/fetchData.php'
PRISM_request_URL

'https://prism.oregonstate.edu/fetchData.php'

PRISM_params = r'type=all_bil&kind=normals&spatial=4km&elem=ppt&temporal=annual'
PRISM_params

final_PRISM_path = PRISM_request_URL + '?' + PRISM_params

print(final_PRISM_path)

PRISM_post_request = requests.post(final_PRISM_path)

PRISM_post_request

ourzipfile = zipfile.ZipFile(
    io.BytesIO(
        PRISM_post_request.content)
)

ourzipfile

bilsfolder = os.path.join(working_dir, 'bils')
bilsfolder

ourzipfile.extractall(bilsfolder)

arcpy.conversion.RasterToOtherFormat(r"'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_01_bil.bil';'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_02_bil.bil';'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_03_bil.bil';'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_04_bil.bil';'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_05_bil.bil';'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_06_bil.bil';'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_07_bil.bil';'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_08_bil.bil';'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_09_bil.bil';'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_10_bil.bil';'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_11_bil.bil';'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_12_bil.bil';'C:\Users\siyal\Desktop\Lab 02\bils\PRISM_ppt_30yr_normal_4kmM3_annual_bil.bil'", r"C:\Users\siyal\Desktop\Lab 02", "TIFF")

arcpy.management.CreateMosaicDataset(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS (Lab 02)\ArcGIS (Lab 02).gdb", "Mosaic", 'PROJCS["datum_D_North_American_1983_HARN_UTM_Zone_15N",GEOGCS["GCS_datum_D_North_American_1983_HARN",DATUM["D_unknown",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["false_easting",500000.0],PARAMETER["false_northing",0.0],PARAMETER["central_meridian",-93.0],PARAMETER["scale_factor",0.9996],PARAMETER["latitude_of_origin",0.0],UNIT["Meter",1.0]],VERTCS["NAVD88 - Geoid03 (Meters)",VDATUM["unknown"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]]', None, '', "NONE", None)

arcpy.management.AddRastersToMosaicDataset(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS (Lab 02)\ArcGIS (Lab 02).gdb\Mosaic", "Raster Dataset", r"'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_01_bil.tif';'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_02_bil.tif';'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_03_bil.tif';'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_04_bil.tif';'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_05_bil.tif';'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_06_bil.tif';'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_07_bil.tif';'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_08_bil.tif';'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_09_bil.tif';'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_10_bil.tif';'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_11_bil.tif';'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_12_bil.tif';'C:\Users\siyal\Desktop\Lab 02\PRISM_ppt_30yr_normal_4kmM3_annual_bil.tif'", "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", None, 0, 1500, None, '', "SUBFOLDERS", "ALLOW_DUPLICATES", "NO_PYRAMIDS", "NO_STATISTICS", "NO_THUMBNAILS", '', "NO_FORCE_SPATIAL_REFERENCE", "NO_STATISTICS", None, "NO_PIXEL_CACHE", r"C:\Users\siyal\AppData\Local\ESRI\rasterproxies\Mosaic")

arcpy.management.CalculateField(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS (Lab 02)\ArcGIS (Lab 02).gdb\mosaic", "Timestamp", "DateAdd(Date(2020,0,1),$feature.OBJECTID-1,'month')","ARCADE", '', "TEXT")

arcpy.management.CalculateField(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS (Lab 02)\ArcGIS (Lab 02).gdb\mosaic", "Timestamp", "$feature.OBJECTID", "ARCADE", '', "TEXT", "NO_ENFORCE_DOMAINS")

arcpy.md.BuildMultidimensionalInfo("mosaic", "Variable", "Timestamp # #", "mosaic # #")

arcpy.md.MakeMultidimensionalRasterLayer(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS (Lab 02)\ArcGIS (Lab 02).gdb\mosaic", "mosaic_MultidimLayer12", "mosaic", "ALL", None, None, '', '', '', None, '', '-13917257.2777 2761917.52169259 -7400428.75412497 6435460.7179 PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]', "DIMENSIONS", None)
