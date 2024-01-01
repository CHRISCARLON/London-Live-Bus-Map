import streamlit as st
from bod_api import fetch_and_save_bus_data
from xml_to_parquet import xml_to_parquet
from geo_prep import load_data, create_gdf
from create_map import plot_on_map
from streamlit_folium import folium_static


def title_page():
    st.markdown("# :bus: Live London Bus Map Version 1.1")
    st.warning("""
    **Contains public sector information licensed under the Open Government Licence v3.0.**
    \n**The Public Service Vehicles (Open Data) (England) Regulations 2020 require me to state that:**
    \n- information has been taken from the bus open data digital service internet site
    \n- while the Secretary of State strives to preserve the integrity and quality of information on 
    the bus open data digital service internet site, they cannot warrant the accuracy or quality of the information 
    on the site
    \n- This app does not have the endorsement, affiliation, support or approval of the Secretary of State.
    """)
    st.markdown("""
    **Version 1 Features:**
    - Live location updates of buses in London (and surrounding areas) using DfT Open Bus Data.
    - Static Folium map. 
    - Option to refresh data to update bus locations. 
    - Markers coloured based on Network Operator: TfL = Red & Others = Blue. 
    """)
    st.markdown("""
    **Version 2 Upcoming Features:**
    - Improved UI: better bus icons and more detailed bus information. 
    - Bus service count: Count the amount of buses currently running for a selected service. 
    - Bus service filter: Filter map based on selected bus service(s) & only refresh locations for the 
    selected bus service(s). 
    - Include NaPTAN data for bus stops as well as timetable and fares data from BODS. 
    - Option to select dark mode for night buses: Change to a dark base map depending on the time of day. 
    """)
    st.markdown("""
    **Version 3 Upcoming Features:**
    - Post code search: Zoom to an area based on a post code. 
    - Incorporate and define 'Zones of Interest': For example, areas of historic high congestion and disruption.
    - include bus routes for each TFL service. 
    """)


def app():
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

        folium_static(updated_map, width=1100, height=800)

    # Refresh button for manual data reload
    if st.button('🔄 Load Data and Refresh Data'):
        refresh_data()


def main():
    st.set_page_config(layout="wide")
    page = st.sidebar.radio("**Please select a page:**", [":house: Home Page", ":cd: Bus App"])

    if page == ":house: Home Page":
        title_page()
    elif page == ":cd: Bus App":
        app()


if __name__ == "__main__":
    main()
