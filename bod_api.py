import requests


def fetch_and_save_bus_data(api_url, bounding_box, api_key, output_filename):
    # Parameters for the API request
    params = {
        "boundingBox": bounding_box,
        "api_key": api_key
    }

    # Making the API call
    try:
        response = requests.get(api_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the XML response to a file
            with open(output_filename, "wb") as file:
                file.write(response.content)
            print(f"Data saved to {output_filename}")
        else:
            print(f"Failed to retrieve data: Status code {response.status_code}, Response: {response.text}")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
