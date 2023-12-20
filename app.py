import streamlit as st
from bod_api import fetch_and_save_bus_data
from xml_to_parquet import xml_to_parquet
from geo_prep import load_data, create_gdf
from create_map import plot_on_map
from streamlit_folium import folium_static


def main():
    st.set_page_config(layout="wide")
    st.markdown("# :bus: Live London Bus Map (Version 1)")
    st.markdown("""
    **Version 1 Features:**
    - Live location updates of buses in London (and surrounding areas) using DfT Open Bus Data.
    - Static Folium map. 
    - Option to refresh data for real-time tracking.
    - Markers coloured based on Network Operator: TfL = Red & Others = Blue. 
    """)
    st.markdown("""
    **Version 2 Upcoming Features:**
    - Improve UI via dynamic map updates: When a user clicks the refresh button only the bus markers will update and 
    the base map will not reload.
    - Bus service count: Count the amount of buses currently running for a selected service. 
    - Bus service filter: Filter map based on selected bus service(s) & only refresh locations for the 
    selected bus service(s). 
    - Option to select dark mode for night buses: Change to a dark base map depending on the time of day. 
    """)
    st.markdown("""
    **Version 3 Upcoming Features:**
    - Post code search: Zoom to an area based on a post code. 
    - Incorporate and define 'Zones of Interest': For example, areas of historic high congestion and disruption.
    - Show published bus routes for each TFL service: Description TBC
    """)

    # Function to fetch and process data
    def refresh_data():
        api_key = st.secrets["tfl_bus"]["api_key"]
        api_url = st.secrets["tfl_bus"]["api_url"]
        bounding_box = st.secrets["tfl_bus"]["bounding_box"]

        fetch_and_save_bus_data(api_url, bounding_box, api_key, "bus_location_data.xml")
        xml_to_parquet("bus_location_data.xml", "bus_location_data.parquet")

        data = load_data("bus_location_data.parquet")
        geo_df = create_gdf(data)
        updated_map = plot_on_map(geo_df)

        folium_static(updated_map, width=1500, height=800)

    # Refresh button for manual data reload
    if st.button('🔄Refresh Data'):
        refresh_data()

    # Load data and update map automatically on first load
    refresh_data()


if __name__ == "__main__":
    main()

