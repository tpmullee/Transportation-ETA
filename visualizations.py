import folium

def plot_route(route_id: str, start: tuple, end: tuple, route_name: str) -> None:
    """
    Creates an interactive map visualization for a given route and saves it as an HTML file.

    Args:
        route_id (str): Unique identifier for the route.
        start (tuple): Starting location coordinates (latitude, longitude).
        end (tuple): Ending location coordinates (latitude, longitude).
        route_name (str): Name of the route to display on the map.

    Returns:
        None: The map is saved as an HTML file named `route_<route_id>.html`.
    """
    # Initialize a Folium map centered between the start and end points
    mid_lat = (start[0] + end[0]) / 2
    mid_lon = (start[1] + end[1]) / 2
    route_map = folium.Map(location=[mid_lat, mid_lon], zoom_start=7)

    # Add markers for start and end points
    folium.Marker(location=start, popup=f"Start: {route_name}", icon=folium.Icon(color="green")).add_to(route_map)
    folium.Marker(location=end, popup=f"End: {route_name}", icon=folium.Icon(color="red")).add_to(route_map)

    # Add a line connecting the start and end points
    folium.PolyLine([start, end], color="blue", weight=2.5, opacity=0.8).add_to(route_map)

    # Save the map as an HTML file
    output_file = f"route_{route_id}.html"
    route_map.save(output_file)
    print(f"Route visualization saved as {output_file}.")
