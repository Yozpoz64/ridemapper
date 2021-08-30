'''
GPX Plotter

plots GPX files on to a folium/leaflet map
read full readme on GitHub repo

Created by: Sophie Kolston
'''

# dependencies
import haversine as hs
import folium
import folium.plugins
import gpxpy

# constants
TITLE = 'My Cycling Map'
AUCKLAND = (-36.88, 174.75)
ZOOM = 12
TILES = 'Stamen Terrain'


class mapper():
    def __init__(self, automate=False):
        
        if automate:
            self.map = self.get_webmap()
    
    
    # get folium map
    def get_webmap(self, show_title=True, title=TITLE, fullscreen_button=True,
                   mouse_position=True, measure_control=True, 
                   centre=AUCKLAND, zoom=ZOOM, tiles=TILES):
        
        # set map height lower if title is requested
        height = '85%' if show_title else '100%'
        
        # get folium map
        folium_map = folium.Map(location=centre, zoom_start=zoom,
                                tiles=tiles, control_scale=True, 
                                height=height)
        
        # add title if required
        if show_title:
            title_html = ('<h3 align="center" style="font-size:20px"><b>{}</b></h3>'
                     .format(title))
            folium_map.get_root().html.add_child(folium.Element(title_html))
            
        # add other elements if required
        if fullscreen_button:
            folium.plugins.Fullscreen(position='topleft').add_to(folium_map)
        if mouse_position:
            folium.plugins.MousePosition(position='topright').add_to(folium_map)
        if measure_control:
            folium.plugins.MeasureControl(primary_length_unit='meters',
            secondary_length_unit='kilometers', primary_area_unit='sqmeters',
            secondary_area_unit ='sqkilometers').add_to(folium_map)
        
        return folium_map

