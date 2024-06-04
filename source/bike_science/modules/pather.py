import geopandas as gpd
import pandas as pd
import json

def graphhopper_pather(POI_gdf, json_filename):

    graph_hopper_key = '5ff51c95-019f-422b-aab5-777d90552c28'

    url = 'https://graphhopper.com/api/1/route?key=' + graph_hopper_key + \
    '&point={},{}&point={},{}&vehicle=bike&elevation=true&type=json&points_encoded=false'

    gdf = gpd.GeoDataFrame(geometry=[])

    for index, row in POI_gdf.iterrows():
        data_from_request = graphopper_request(url)
        gdf = gdf.append(data_from_request, ignore_index=True)

    gdf = convert_list_columns_to_str(gdf)

    save_json(gdf, json_filename)

def paths_extractor(json_filename):

    with open(json_filename, 'r') as file:
        data = json.load(file)

    coordinates = data['features'][0]['properties']['paths'][0]['points']['coordinates']
    
    return coordinates