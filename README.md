**NAME**:
The creation of a web map







**DESCRIPTION**:
*The map was created for showing 10 closest location according to yours geolocation and given year
when the film was taken. 
Also it containes 3 layers, which you can easily switch.
For this program I used folium, geopy and argparse libraries*







**USAGE**:

*The program can be launched in command line with help of argparse*: >>> python(3) main.py year latitude longitude path

	Your input parameters are: year,latitude, longitude, path
year - when film was taken, type (str)

latitude - of your location , type (float)

longitude - of your location , type (float)

path - path to file , type (str)*





**VISUAL**:

*This is image of my map 
![programming1](https://user-images.githubusercontent.com/92577132/153509641-816f4d97-8d27-4f46-8bd4-87a6df3704e0.png)



**Features of my map**:

> 1.layer control
![layer_control](https://user-images.githubusercontent.com/92577132/153510342-f7b291ab-55bd-4def-b7b5-fdb4395db5c9.png)

> 2. colored points with icons with name of films
![points](https://user-images.githubusercontent.com/92577132/153510507-dae3f8bf-b634-4c7d-8e7e-768a508ec46d.png)

> 3. tools for operating with map
![tools](https://user-images.githubusercontent.com/92577132/153510631-804a4d27-977d-40b6-bb15-88c574f9fbc7.png)

> 4. mini map
![mini_map](https://user-images.githubusercontent.com/92577132/153510678-653d8526-1957-48ce-a668-1f76d3d53176.png)

> 5. point with icon that you are here
![my_icon](https://user-images.githubusercontent.com/92577132/153510883-c02fa91c-beb3-4ab7-9e09-40337aeadcf4.png)




**PS: Some troubles can happen with time for operating. For finding the distance I use geopy.distance.distance,
because it's convinient. In case of troubles let me now.**


