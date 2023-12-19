import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


def load_data(file):
    df = pd.read_parquet(file)
    return df


def create_gdf(df, lon_col='Longitude', lat_col='Latitude'):
    """
    Convert a DataFrame with longitude and latitude columns to a GeoDataFrame.

    Parameters:
    df (pandas.DataFrame): DataFrame with longitude and latitude.
    lon_col (str): Name of the column with longitude data.
    lat_col (str): Name of the column with latitude data.

    Returns:
    geopandas.GeoDataFrame
    """
    # Create a geometry column from longitude and latitude
    geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
    geo_df = gpd.GeoDataFrame(df, geometry=geometry)
    geo_df.set_crs(epsg=4326, inplace=True)
    return geo_df
