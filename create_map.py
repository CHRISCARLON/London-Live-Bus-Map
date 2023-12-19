import folium
from folium.plugins import MarkerCluster


def plot_on_map(geo_df):
    # Create a base map with a default location
    base_map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)

    marker_cluster = MarkerCluster().add_to(base_map)

    # Iterate over each row in the GeoDataFrame and add markers
    for index, row in geo_df.iterrows():
        # Set the colour based on OperatorRef
        icon_color = 'red' if row['OperatorRef'] == 'TFLO' else 'blue'

        # Create popup content
        popup_content = f"""
        <b>Bus Route:</b> {row['PublishedLineName']}<br>
        <b>Direction:</b> {row['DirectionRef']}<br>
        <b>Operator:</b> {row['OperatorRef']}
        """

        # Create and add a markers to the map
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            icon=folium.Icon(color=icon_color, icon="bus", prefix="fa"),
            popup=popup_content,
            tooltip=row['PublishedLineName']
        ).add_to(marker_cluster)

    return base_map
