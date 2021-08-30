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
import glob
import os

# constants
TITLE = 'My Cycling Map'
AUCKLAND = (-36.88, 174.75)
ZOOM = 12
TILES = 'Stamen Terrain'


class mapper():

    # automate below functions (if requested)
    def automatic_map(self, folder):
        self.map = self.get_webmap()
        self.map_gpxs(self.map, folder)
        self.save_webmap(self.map)
    
    # get folium map
    def get_webmap(self, show_title=True, title=TITLE, fullscreen_button=True,
                   mouse_position=True, measure_control=True, 
                   centre=AUCKLAND, zoom=ZOOM, tiles=TILES):
        
        # add title variable locally for later use in saving
        self.show_title = show_title
        
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
        
        # return map object
        return folium_map
    
    
    # calculates distance (haversine) between sets of coordinates
    def calculate_distance(self, coords):
        all_distances = []
        
        # I think this equation is flawed and does not include last couple of points
        for i in range(len(coords)):
            if i != len(coords) - 1:
                dist = hs.haversine(coords[i], coords[i + 1], unit=hs.Unit.METERS)
                all_distances.append(dist)
                
        # returns as km value with 2 dp
        return round((sum(all_distances) / 1000), 2)
    
    
    # gets polyline (set of coordinates) from gpx, as well as metadata
    def get_gpxdata(self, gpx_file):
        gpx_raw = open(gpx_file, 'r')
        gpx = gpxpy.parse(gpx_raw)
        
        points = []
        times = []
        
        raw_start_time = gpx.tracks[0].segments[0].points[0].time
        raw_end_time = gpx.tracks[0].segments[0].points[-1].time
        
        length_hours = str(round((raw_end_time - raw_start_time)
                                 .seconds / 60 / 60, 2))
        length_mins = str((float(length_hours.split('.')[1]) * 0.01) 
                          * 60).split('.')[0]
        length = '{} hour{} {} minutes'.format(length_hours[0], 's' if int(length_hours[0]) > 1 else '', length_mins)
        
        point_count = len(gpx.tracks[0].segments[0].points)
        
        date = raw_start_time.strftime('%A %-d %B (%d-%m-%Y)')

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append(tuple([point.latitude, point.longitude]))
                    times.append(point.time)
    
        distance = self.calculate_distance(points)
      
        speed = round(distance / float(length_hours), 2)
        
        track_data = {
            'points': points,
            'times': times,
            'date': date,
            'length': length,
            'point n': point_count,
            'distance': distance,
            'speed': speed}
        
        return track_data


    def map_gpxs(self, map_object, folder, line_type='antpath', line_weight=5, 
                 line_opacity=0.5):
        self.distance = -1
        
        '''
        NEED TO ADD COLOUR CHANGING SUPPORT
        '''
        colour = 'blue'
        
        try:
            self.data = self.get_files(folder)
            
            # for every gpx file in the given folder
            for gpx_file in self.data:
                # get coords and metadata
                track_data = self.get_gpxdata(gpx_file)
                
                # get raw coords
                points = track_data['points']
                
                # add distance to total
                self.distance += track_data['distance']
                
                # html for popup
                popup_string = ('<b>{}</b><br><br><b>Date:</b> {}<br><b>'
                            'Ride length:</b> {}<br><b>Ride distance:</b> {}km'
                            '<br><b>Average speed:</b> {}km/h<br><b>Total GPS '
                            'points:</b> {}'
                            .format(os.path.basename(gpx_file), track_data['date'], 
                                    track_data['length'], track_data['distance'], 
                                    track_data['speed'], track_data['point n']))
                
                if line_type.lower() == 'antpath':
                    # set antpath delay to be proportional to the rider speed
                    antpath_speed = 4000 - (track_data['speed'] * 100)
                    
                    # add antpath to map
                    path = folium.plugins.AntPath(points, delay=antpath_speed, 
                        weight=line_weight, dashArray=(10, 200), colour='blue', 
                        opacity=line_opacity,
                        tooltip=folium.Html(popup_string, script=True).render()
                        ).add_to(map_object)
                        
                    path.options.update(dashArray=[1, 12],
                                        hardwareAcceleration=True,
                                        pulseColor='#3f4145')
                         
                elif line_type.lower() == 'polyline':
                    # add polyline to map
                    folium.PolyLine(points, color=colour, weight=line_weight,
                                    opacity=line_opacity, 
                                    popup=folium.Html(popup_string, script=True)
                                    .render()).add_to(map_object)
                    
                else:
                    print('Error: line type not supported')
                    break
            
        except Exception as e:
            print('Error opening file(s): ', e)
    
    
    # get all gpxs in a folder
    def get_files(self, folder):
        return glob.glob(folder + '*.gpx')
    
    
    # save map
    def save_webmap(self, map_object, filename='map.html'):
        if self.show_title:
            if self.distance > -1:
                map_object.save(filename)
                file = open(filename, 'a')
                subtitle_html = ('<center style="margin-top:0.5cm;"><b>'
                                 'Total distance: </b>{}km</center>'
                                 .format(self.distance))
                file.write(subtitle_html)
        else:
            map_object.save(filename)
    
    

