# RideMapper

### Description
A Python module that maps your .gpx files in a painless, user-friendly way. Loads any folder of .gpx files, parses and converts the files into readable coordinates, then maps the coordinates with summary statistics as tooltips.

Created by Sophie Kolston

### Usage
You can start off by running example.py, which access the .gpx files in the example_data folder and creates an antpath map.

```python
# import ridemapper module
from gpx_plotter import mapper

# get instance of mapping object
gpx_mapper = mapper()

# build map using .gpx files in folder
gpx_mapper.automatic_map('example_data/')
```

You can access most of the folium/leaflet arguments through the class, have a look at the source code to see what is automatically set. Once you have tested the example, you can customize your map by running the functions manually, step-by-step. Simply import the module and go from there. Here you can save the map object itself and add other layers if you need, along with anything else a standard folium map object can allow.

```python
# get a folium map object
m = gpx_mapper.get_webmap(tiles='OpenStreetMap')

# call the mapping function. here are some examples of arguments that can be put through
gpx_mapper.map_gpxs(m, 'example_data/', line_weigth=1, line_type='polyline')

# save the map. this is used in place of the default Folium save as it embeds the title
gpx_mapper.save_webmap(m, filename='myridemap.html')
```

### Example 
The example file can be viewed on the GitHub pages for this repository: https://yozpoz64.github.io/ridemapper/map.html

Here is a screenshot of that site taken in version 1:
![Example output](https://github.com/Yozpoz64/ridemapper/blob/182636dda99df708e21466ff8e970f1d6b628fdc/example_ss.png)


### Dependencies
These modules are required to run ridemapper. They can be installed with pip.
* Folium (and plugins) - Builds Leaflet HTML maps ([Project](https://github.com/python-visualization/folium), [PyPi](https://pypi.org/project/folium/))
* GpxPy - Parses and manipulates .gpx files ([Project](https://github.com/tkrajina/gpxpy), [PyPi](https://pypi.org/project/gpxpy/))


