import requests

url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=44.976248%2C-93.229443&radius=25000&type=restaurant&keyword=restaurant&key=MY_API_KEY"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

import pandas
import json 
r_json=response.json()["results"]

df=pandas.DataFrame(columns=("Name", "Latitude","Longitude"))

for feature in range(len(r_json)):
    name=[r_json[feature]["name"]]
    Latitude=[r_json[feature]["geometry"]["location"]["lat"]]
    Longitude=[r_json[feature]["geometry"]["location"]["lng"]]
    
    df.loc[feature]=name+Latitude+Longitude
    
df.head()

import requests
import pandas as pd

base_ndawn_url = "https://ndawn.ndsu.nodak.edu/table.csv"

master_params = {
"station" : "104",
"variable" : "mdavt",
"dfn" : "",
"year" : "2020",
"ttype" : "monthly",
"quick_pick" : "",
"begin_date" : "2020-01",
"count" : "12"}

req_response = requests.get(base_ndawn_url, params = master_params)

with open ("NameForNewCSVFile.csv", "w") as newCSV_txt:
    newCSV_txt.write(req_response.content.decode('utf-8'))

peek = pd.read_csv('NameForNewCSVFile.csv', skiprows = 3)
peek.head()

import requests
import io
import zipfile
import pandas as pd
import os

mn_geospatial = "https://resources.gisdata.mn.gov/pub/gdrs/data/"

rqst_object = requests.get(mn_geospatial)
rqst_object

rqst_text = rqst_object.text
rqst_text

rice_county_adresses = r'https://resources.gisdata.mn.gov/pub/gdrs/data/pub/us_mn_co_rice/loc_addresses.zip'
rice_county_adresses_shp = r'https://resources.gisdata.mn.gov/pub/gdrs/data/pub/us_mn_co_rice/loc_addresses/shp_loc_addresses.zip'

outputpath = r'C:\Users\siyal\ArcGISLab01'

post_req_obj = requests.post(rice_county_adresses_shp)

post_req_obj.content

io.BytesIO(post_req_obj.content)

zipster = zipfile.ZipFile(io.BytesIO(post_req_obj.content))

zipster.extractall(outputpath)

arcpy.ListFiles()

arcpy.ListFeatureClasses()

arcpy.conversion.ExportFeatures
