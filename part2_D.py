import folium
# import pandas as pd
import csv

map_osm = folium.Map(location=[40.0031,-94.5882],zoom_start=3)
# state_geo = r'usa_tweets.csv'
#
# state_data = pd.read_csv(state_geo)
with open('usa_tweets.csv', newline='' ) as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        if not ''.join(row) == 'geo':
            r = ''.join(row).split(',')
            print(r[0].replace('"[', ''))
            print(float(r[1].replace(']"', '')))

            folium.CircleMarker([float(r[0].replace('"[', '')), float(r[1].replace(']"', ''))], radius=2).add_to(map_osm)

map_osm.save('map.html')