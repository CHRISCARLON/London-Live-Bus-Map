import xml.etree.ElementTree as ET
import pandas as pd


def xml_to_parquet(xml_data, output_file):
    # Parse the XML data
    tree = ET.parse(xml_data)
    root = tree.getroot()

    # Define the namespace
    ns = {'siri': 'http://www.siri.org.uk/siri'}

    # List to hold all VehicleActivity data
    all_vehicle_activities = []

    # Find all VehicleActivity elements
    for vehicle_activity in root.findall('.//siri:VehicleMonitoringDelivery/siri:VehicleActivity', ns):
        data = {}

        # Extract basic information
        data['RecordedAtTime'] = vehicle_activity.find('.//siri:RecordedAtTime', ns).text
        data['ItemIdentifier'] = vehicle_activity.find('.//siri:ItemIdentifier', ns).text
        data['ValidUntilTime'] = vehicle_activity.find('.//siri:ValidUntilTime', ns).text

        # Extract MonitoredVehicleJourney information
        mvj = vehicle_activity.find('.//siri:MonitoredVehicleJourney', ns)
        if mvj is not None:
            # Extract information with checks for None
            for field in ['LineRef', 'DirectionRef', 'PublishedLineName', 'OperatorRef', 'OriginRef',
                          'OriginName', 'DestinationRef', 'DestinationName', 'OriginAimedDepartureTime',
                          'DestinationAimedArrivalTime', 'BlockRef', 'VehicleRef']:
                element = mvj.find(f'.//siri:{field}', ns)
                data[field] = element.text if element is not None else None

            # VehicleLocation
            vehicle_location = mvj.find('.//siri:VehicleLocation', ns)
            if vehicle_location is not None:
                for coord in ['Longitude', 'Latitude']:
                    element = vehicle_location.find(f'.//siri:{coord}', ns)
                    data[coord] = element.text if element is not None else None

        # Extract Extensions information
        extensions = vehicle_activity.find('.//siri:Extensions', ns)
        if extensions is not None:
            vehicle_journey = extensions.find('.//siri:VehicleJourney', ns)
            if vehicle_journey is not None:
                # Extract information with checks for None
                for field in ['TicketMachineServiceCode', 'JourneyCode', 'VehicleUniqueId']:
                    element = vehicle_journey.find(f'.//siri:{field}', ns)
                    data[field] = element.text if element is not None else None

        # Append the data to the all_vehicle_activities list
        all_vehicle_activities.append(data)

    # Create a DataFrame for all VehicleActivities
    df = pd.DataFrame(all_vehicle_activities)

    # Save the DataFrame as a single Parquet file
    df.to_parquet(output_file, index=False)

    return df

