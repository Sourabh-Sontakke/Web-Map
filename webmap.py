import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

wonders = pandas.read_csv("wonders.txt")
w_lat = list(wonders["LAT"])
w_lon = list(wonders["LON"])
w_img = list(wonders["IMAGE"])
w_name = list(wonders["NAME"])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[38.58, -99.09], zoom_start=6)

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el, nm in zip(lat, lon, elev, name):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=f'{el} m', tooltip=str(nm),
     fill_color=color_producer(el), color='grey', fill_opacity=0.7))

fgw = folium.FeatureGroup(name="7 Wonders")

for lt, ln, im, nm in zip(w_lat, w_lon, w_img, w_name):
    fgw.add_child(folium.Marker(location=[lt, ln], popup=f"<h1>{nm}</h1><BR><img src='{im}'>", tooltip=nm))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgp)
map.add_child(fgv)
map.add_child(fgw)
map.add_child(folium.LayerControl())

map.save("map1.html")