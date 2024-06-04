#1:1 point to closest point

import geopandas as gpd
import pandas as pd

def sorter11(polygons1, polygons2, key_factor):
    
    intersecting_gdf = gpd.GeoDataFrame(columns=polygons1.columns)

    polygon1_center_points = []
    polygon2_center_points = []

    for index, polygon2 in polygons2.iterrows():
        intersects = polygons1['geometry'].intersects(polygon2['geometry'])

        if intersects.any():    
            intersection_list = polygons1[intersects]
            important_sector = intersection_list.loc[intersection_list[key_factor].idxmax()]
            intersecting_gdf = pd.concat([intersecting_gdf, important_sector.to_frame().T], ignore_index=True)

            polygon1_center = important_sector['geometry'].centroid
            polygon1_center_points.append(polygon1_center)

            polygon2_center = polygon2['geometry'].centroid
            polygon2_center_points.append(polygon2_center)

    intersecting_gdf['polygon2_center'] = polygon2_center_points
    intersecting_gdf['polygon1_center'] = polygon1_center_points

    return intersecting_gdf


def sorter1n(polygons1, polygons2):
    # polygons1 = gpd.read_file("polygons1.geojson", driver='GeoJSON')
    # polygons1.crs = {'init': 'epsg:31983'}

    # polygons2 = gpd.read_file("POIs.json", driver='GeoJSON')
    # polygons2.to_crs(epsg='31983', inplace=True)

    result_dfs = []

    for index1, polygon1 in polygons1.iterrows():
        intersecting_polygons2 = polygons2[polygons2.intersects(polygon1['geometry'])]

        for index2, polygon2 in intersecting_polygons2.iterrows():
            centroid1 = polygon1['geometry'].centroid
            centroid2 = polygon2['geometry'].centroid

            result_dfs.append(pd.DataFrame({
                'polygon1_centroid': [centroid1],
                'polygon2_centroid': [centroid2]
            }))

    result_df = pd.concat(result_dfs, ignore_index=True)

    result_gdf1 = gpd.GeoDataFrame(geometry=result_df['polygon1_centroid'])
    result_gdf2 = gpd.GeoDataFrame(geometry=result_df['polygon2_centroid'])
    
    return result_gdf1, result_gdf2
