#needed to make web requests
import requests

#store the data we get as a dataframe
import pandas as pd

#mathematical operations on lists
import numpy as np

import sys

#Define Project Directory

pro_direct = r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS-Lab3p2\ArcGIS-Lab3p2.gdb"

arcpy.env.workspace = pro_direct

#For testing purpose

arcpy.env.workspace

base_ndawn_url = "https://ndawn.ndsu.nodak.edu/table.csv?station=78&station=111&station=98&station=174&station=142&station=138&station=161&station=9&station=10&station=118&station=56&station=11&station=12&station=58&station=13&station=84&station=55&station=7&station=87&station=14&station=15&station=96&station=16&station=137&station=124&station=143&station=17&station=85&station=140&station=134&station=18&station=136&station=65&station=104&station=99&station=19&station=129&station=20&station=101&station=81&station=21&station=97&station=22&station=75&station=2&station=172&station=139&station=23&station=62&station=86&station=24&station=89&station=126&station=93&station=90&station=25&station=83&station=107&station=156&station=77&station=26&station=70&station=127&station=27&station=132&station=28&station=29&station=30&station=31&station=102&station=32&station=119&station=4&station=80&station=33&station=59&station=105&station=82&station=34&station=72&station=135&station=35&station=76&station=120&station=141&station=109&station=36&station=79&station=71&station=37&station=38&station=39&station=130&station=73&station=40&station=41&station=54&station=69&station=113&station=128&station=42&station=43&station=103&station=116&station=88&station=114&station=3&station=163&station=64&station=115&station=67&station=44&station=133&station=106&station=100&station=121&station=45&station=46&station=61&station=66&station=74&station=60&station=125&station=8&station=47&station=122&station=108&station=5&station=152&station=48&station=68&station=49&station=50&station=91&station=117&station=63&station=150&station=51&station=6&station=52&station=92&station=112&station=131&station=123&station=95&station=53&station=57&station=149&station=148&station=110&variable=ddmxt&variable=ddmnt&variable=ddavt&dfn=&ttype=daily&quick_pick=30_d"

#requests

data_req = requests.get(base_ndawn_url)

#open 

with open('AvgTemp_AllStations.csv', 'w') as AvgTempsAll:
    AvgTempsAll.write(data_req.content.decode('utf-8')) #decode with unicode 8 parameters
avg_temp_df = pd.read_csv('AvgTemp_AllStations.csv', skiprows = 5)
avg_temp_df = avg_temp_df.iloc[1:] #initializes df from row 2 to skip the messy labels in row index 0
avg_temp_df

#save table as csv
avg_temp_df.to_csv('AveTempOfAllStat.csv')

#Import CSV as Points in ArcPro
arcpy.management.XYTableToPoint(r"C:\Users\siyal\Desktop\1. UMN MGIS\1. Semesters\1st Semester\2. ArcGIS I\1. Labs\Lab 3\AveTempOfAllStat.csv", r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS-Lab3p2\ArcGIS-Lab3p2.gdb\AvgTemp_AllStations_XYTableToPoint", "Longitude", "Latitude", None, 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')

#IDW
#Average Temperature as Z value field
IDW_AvgTemp = arcpy.sa.Idw("AvgTemp_AllStations_XYTableToPoint", "Avg_Temp", 0.0144790399999999, 2, "VARIABLE 12", None); IDW_AvgTemp.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS-Lab3p2\ArcGIS-Lab3p2.gdb\IDW_AvgTemp")

#Natural Neighbor
#Avg.Temperature
NaturalNeigh_AvgTemp = arcpy.sa.NaturalNeighbor("AvgTemp_AllStations_XYTableToPoint", "Avg_Temp", 0.0144790399999999); NaturalNeigh_AvgTemp.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS-Lab3p2\ArcGIS-Lab3p2.gdb\NaturalNeigh_AvgTemp")

#Ordinary Origins
#Avg.Temperature
Kriging_AvgTemp = arcpy.sa.Kriging("AvgTemp_AllStations_XYTableToPoint", "Avg_Temp", "Spherical # # # #", 0.0144790399999999, "VARIABLE 12", None); Kriging_AvgTemp.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS-Lab3p2\ArcGIS-Lab3p2.gdb\Kriging_AvgTemp")

#Spline
#Avg.Temperature
Spline_AvgTemp = arcpy.sa.Spline("AvgTemp_AllStations_XYTableToPoint", "Avg_Temp", 0.0144790399999999, "REGULARIZED", 0.1, 12); Spline_AvgTemp.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS-Lab3p2\ArcGIS-Lab3p2.gdb\Spline_AvgTemp")

#IDW
#Max.Temperature
IDW_MaxTemp = arcpy.sa.Idw("AvgTemp_AllStations_XYTableToPoint", "Max_Temp", 0.0144790399999999, 2, "VARIABLE 12", None); IDW_MaxTemp.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS-Lab3p2\ArcGIS-Lab3p2.gdb\IDW_MaxTemp")

#Min.Temperature
IDW_MinTemp = arcpy.sa.Idw("AvgTemp_AllStations_XYTableToPoint", "Min_Temp", 0.0144790399999999, 2, "VARIABLE 12", None); IDW_MinTemp.save(r"C:\Users\siyal\Documents\ArcGIS\Projects\ArcGIS-Lab3p2\ArcGIS-Lab3p2.gdb\IDW_MinTemp")


