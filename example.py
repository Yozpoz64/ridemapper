import webbrowser
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

from gpx_plotter import mapper



gpx_mapper = mapper()
gpx_mapper.automatic_map('example_data/')



