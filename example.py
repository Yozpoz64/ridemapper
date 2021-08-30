import webbrowser
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

from gpx_plotter import mapper

gpx_mapper = mapper()


m = gpx_mapper.get_webmap()
m.save('example.html')
webbrowser.open('example.html')
