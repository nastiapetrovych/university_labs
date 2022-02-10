from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from folium import plugins
import argparse
"""
The creation of web-map, created based on file with films according to the distance
"""
# Here I create argparse
parser = argparse.ArgumentParser(description='This is my argparse')
parser.add_argument('year', type=str,
                    help='gives a year')
parser.add_argument('latitude', type=float,
                    help='gives a latitude of our location')
parser.add_argument('longitude', type=float,
                    help='gives a longitude of our location')
parser.add_argument('path', type=str,
                    help='gives the path to the file')


def reading_file(path, year):
    """
    Returns the list of locations
    Here I read file and return list of lists depend on year
    :param path: str
    :param year: str
    :return: list
    """
    with open(path, 'r', encoding='utf -8') as file:
        lst = []
        for line in file:
            if line.startswith('"'):
                lst1 = line.strip('/t').split('"')
                our_year = lst1[-1][2:6]
                if year == our_year:
                    film_name = lst1[1]
                    lst2 = line.strip().split(',')
                    index = len(lst2)
                    location = lst2[index - 2]
                    final_lst = [film_name, our_year, location]
                    lst.append(final_lst)
        my_dict = dict()
        for element in lst:
            if element[1] not in my_dict:
                my_dict[element[1]] = [[element[0], element[2]]]
            else:
                my_lst = [element[0], element[2]]
                my_dict[element[1]].append(my_lst)
        return lst


def coordinates(lst_with_locations_, my_coordinates):
    """
    Here I do s lot of: find the distance,list of coordinates of the
    10 closest films in tuple and distance(sorted by distance)
    Returns list with coordinates
    :param lst_with_locations_: list
    :param my_coordinates: tuple
    :return: list
    """
    new_lst = []
    for element in lst_with_locations_:
        geo_location = element[-1]
        geolocator = Nominatim(user_agent='My map')
        geo_loc = geo_location.strip()
        try:
            location = geolocator.geocode(geo_loc)
            coordinate = (location.latitude, location.longitude)
            element.append(coordinate)
            element.append(geodesic(coordinate, my_coordinates).km)
            new_lst.append(element)
        except:
            continue
    my_dict = {}
    for element in new_lst:
        if element[-1] not in my_dict:
            value = [element[0], element[2], element[3]]
            my_dict[element[-1]] = [value]
        else:
            value = [element[0], element[2], element[3]]
            my_dict[element[-1]].append(value)
    dictionary_items = my_dict.items()
    sorted_items = sorted(dictionary_items)
    if len(sorted_items) > 10:
        sorted_items = sorted_items[:9]
    return sorted_items


def creating_map(locations, my_latitude, my_longitude):
    """
    Here I creates a map with 3 layers
    :param locations: list
    :param my_latitude: float
    :param my_longitude: float
    :return: None
    """
    map = folium.Map(tiles="Stamen Terrain", location=[my_latitude, my_longitude], control_scale=True)
    fg = folium.FeatureGroup(name="The places of the nearest location")
    for element in locations:
        latitude = element[1][-1][-1][0]
        longitude = element[1][-1][-1][1]
        index = element[1][-1][0]
        fg.add_child(
            folium.Marker(location=[latitude, longitude], popup=index, icon=folium.Icon(icon='film', color="pink")))
    map.add_child(fg)
    minimap = plugins.MiniMap(toggle_display=True)
    map.add_child(minimap)
    plugins.ScrollZoomToggler().add_to(map)
    plugins.Fullscreen(position="topleft").add_to(map)
    fg2 = folium.FeatureGroup(name="Places")
    fg2.add_child(folium.Marker(location=[my_latitude, my_longitude], popup="Hi,you are here",
                                icon=folium.Icon(color="orange", icon='you are cool one')))
    map.add_child(fg2)
    map.add_child(folium.LayerControl())
    map.save('my_map2.html')


def main():
    """
    This function run all my module using argparse
    """
    args = parser.parse_args()
    path = args.path
    year = args.year
    lst_with_locations = reading_file(path, year)
    my_latitude = float(args.latitude)
    my_longitude = float(args.longitude)
    my_coordinate = (my_latitude, my_longitude)
    locations = coordinates(lst_with_locations, my_coordinate)
    creating_map(locations, my_latitude, my_longitude)


if __name__ == "__main__":
    main()
