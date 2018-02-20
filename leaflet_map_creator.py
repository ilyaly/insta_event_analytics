from geojson import Feature, Point, FeatureCollection
import csv
import geojson


path_to_scv = input('Please enter the path to csv with geocoded locations: ')
output_path = input('Please enter path for the output HTML map: ')
map_type = input('If you want clustring map enter YES if point map enter NO :')



def csv_to_json(path_to_csv):
    features_list = []
    with open(path_to_csv, 'r') as f:
        reader = csv.reader(f)
        pages_list = list(reader)
    for p in pages_list:
        val = p
        j_point = Feature(geometry=Point((float(val[1]),float(val[0]))))
        features_list.append(j_point)
    feature_collection = FeatureCollection(features_list)
    return feature_collection





"""
Function for computing the average coordinate for a GeoJSON object.
"""
def coordinates_center(obj):
    (lon, lat, count) = (0.0, 0.0, 0)
    for feature in obj['features']:
        for (lo, la) in geojson.utils.coords(feature):
            lon += lo
            lat += la
            count += 1
    return [lat/count, lon/count]


"""
Function that nests a GeoJSON object within an HTML document that renders it
as a Leaflet visualization.
"""
def html(obj,\
         src = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.0.3',\
         service = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'\
        ):
    meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    link = '<link rel="stylesheet" href="' + src + '/leaflet.css" />'
    body = '''
	<div id="leaflet" style="width:100vw; height:100vh;"></div>
	<script>\nvar obj = ''' + geojson.dumps(obj, sort_keys=True, indent=2) + ";\n" + '''    </script>
	<script src="''' + src + '''/leaflet.js"></script>
	<script>
      function randomColor() {
        var color = '', letters = '0123456'; //789ABCDEF
        for (var i=0; i<6; i++) {color += letters[Math.floor(Math.random() * letters.length)];}
        return '#' + color;
      }
      var leaflet = L.map('leaflet').setView(''' + str(coordinates_center(obj)) + ''', 2);
      L.tileLayer("''' + service + '''", {
        maxZoom:18, attribution:'', id:'mapbox.light'
      }).addTo(leaflet);
      function onEachFeature(feature, layer) {
        if (feature.properties) {
          var popupContent = "<p>" + feature.properties.name + '-' + feature.properties.osm_id + ".</p>";
          if (feature.properties.popupContent)
              popupContent += feature.properties.popupContent;
          layer.bindPopup(popupContent);
        }
      }
      L.geoJson(obj, {
        filter: function (feature, layer) { return true; },
        onEachFeature: onEachFeature,
        style: function (feature) { return {"color": randomColor()}; },
        pointToLayer:
          function (feature, latlng) {
            return L.circleMarker(latlng, {radius:5, weight:0.1, fillColor:"#6666AA", color:"#6666AA", opacity:0.1, fillOpacity:0.1});
          }
      }).addTo(leaflet);
	</script>'''
    return "<!DOCTYPE html>\n<html>\n  <head>\n    " + meta + "\n    " + link +\
'\n  </head>\n  <body style="width:100%; height:100%; margin:0; padding:0;">' + body + "\n  </body>\n</html>"

def html_clust(obj,\
         src = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.0.3',\
         service = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'\
        ):
    meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    link = '<link rel="stylesheet" href="' + src + '/leaflet.css" />' + '\n' + '<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.3.0/dist/MarkerCluster.Default.css"/>'
    body = '''
	<div id="leaflet" style="width:100vw; height:100vh;"></div>
	<script>\nvar obj = ''' + geojson.dumps(obj, sort_keys=True, indent=2) + ";\n" + '''    </script>
	<script src="''' + src + '''/leaflet.js"></script>
	<script src="https://unpkg.com/leaflet.markercluster@1.3.0/dist/leaflet.markercluster-src.js"></script>
	<script>
      function randomColor() {
        var color = '', letters = '0123456'; //789ABCDEF
        for (var i=0; i<6; i++) {color += letters[Math.floor(Math.random() * letters.length)];}
        return '#' + color;
      }
      var leaflet = L.map('leaflet').setView([49.76782772308692, 33.40609195942309], 2);
      L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom:18, attribution:'', id:'mapbox.light'
      }).addTo(leaflet);
      function onEachFeature(feature, layer) {
        if (feature.properties) {
          var popupContent = "<p>" + feature.properties.name + '-' + feature.properties.osm_id + ".</p>";
          if (feature.properties.popupContent)
              popupContent += feature.properties.popupContent;
          layer.bindPopup(popupContent);
        }
      };
      var markers = L.markerClusterGroup();
      var layer = L.geoJson(obj, {
        filter: function (feature, layer) { return true; },
        onEachFeature: onEachFeature,
        style: function (feature) { return {"color": randomColor()}; },
        pointToLayer:
          function (feature, latlng) {
            return L.circleMarker(latlng, {radius:6, weight:0.1, fillColor:"#6666AA", color:"#6666AA", opacity:0.1, fillOpacity:0.1});
          }
      });
      markers.addLayer(layer);
      leaflet.addLayer(markers)
	</script>'''
    return "<!DOCTYPE html>\n<html>\n  <head>\n    " + meta + "\n    " + link +\
'\n  </head>\n  <body style="width:100%; height:100%; margin:0; padding:0;">' + body + "\n  </body>\n</html>"



def save_html_map(output_path,page):
    output_path = output_path + '\\map.html'
    with open(output_path, "w") as output:
       output.write(page)
    print('Saving to csv has been finished!')
if map_type == 'YES':
    page = html_clust(csv_to_json(path_to_scv))
elif map_type == 'NO':
    page = html(csv_to_json(path_to_scv))
else: print('You have set wrong map type, run script again and set the right type!')

save_html_map(output_path,page)