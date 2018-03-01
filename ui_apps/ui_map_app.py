from geojson import Feature, Point, FeatureCollection
import csv,geojson,sys
from PySide.QtGui import *
from PySide import QtGui


app = QApplication(sys.argv)
w = QWidget()
w.setWindowTitle('Create map')
w.setWindowIcon(QtGui.QIcon('C:\\Users\\Admin\\Desktop\\insta.jpg'))
w.resize(440, 150)

info = QLabel('Выберите *.csv с координатами локаций и задайте путь сохранения, нажмите "Создать карту"\nЗа процессом можно следить в консоли.',w)
info.resize(420,40)
info.move(20,10)

# Create textbox
in_dir = QPushButton('Выберить *.csv с координатами локаций',w)
in_dir .resize(400,20)
in_dir .move(20, 50)

out_dir = QPushButton('Выберить директорию сохранения',w)
out_dir.resize(400,20)
out_dir.move(20,80)

button = QPushButton('Определить локации', w)
button.resize(400,20)
button.move(20, 110)
filelist = []
dirlist = []

def get_in_file():
    direct = QFileDialog.getOpenFileName()
    filelist.append(direct[0])
    return direct
def get_out_dir():
    direct = QFileDialog.getExistingDirectory()
    dirlist.append(direct)
    return direct
def run_app():
    def csv_to_json(path_to_csv):
        features_list = []
        with open(path_to_csv, 'r') as f:
            reader = csv.reader(f)
            pages_list = list(reader)
        for p in pages_list:
            val = p[0]
            val = val.replace('[', '')
            val = val.replace(']', '')
            val = val.replace(',','')
            val = val.split()
            try:
                j_point = Feature(geometry=Point((float(val[1]), float(val[0]))))
                features_list.append(j_point)
            except: pass
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
        return [lat / count, lon / count]

    """
    Function that nests a GeoJSON object within an HTML document that renders it
    as a Leaflet visualization.
    """

    def html(obj, \
             src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.0.3', \
             service='https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png' \
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
            maxZoom:18, attribution:'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>', id:'mapbox.light'
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
        return "<!DOCTYPE html>\n<html>\n  <head>\n    " + meta + "\n    " + link + \
               '\n  </head>\n  <body style="width:100%; height:100%; margin:0; padding:0;">' + body + "\n  </body>\n</html>"

    def html_clust(obj, \
                   src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.0.3', \
                   service='https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png' \
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
          var leaflet = L.map('leaflet').setView(''' + str(coordinates_center(obj)) + ''', 2);
          L.tileLayer("''' + service + '''", {
            maxZoom:18, attribution:'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>', id:'mapbox.light'
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
        return "<!DOCTYPE html>\n<html>\n  <head>\n    " + meta + "\n    " + link + \
               '\n  </head>\n  <body style="width:100%; height:100%; margin:0; padding:0;">' + body + "\n  </body>\n</html>"

    def save_html_map(output_path, page):
        output_path = output_path + '\\map.html'
        with open(output_path, "w") as output:
            output.write(page)
        print('Saving to csv has been finished!')


    page = html_clust(csv_to_json(filelist[0]))
    save_html_map(dirlist[0], page)

in_dir.clicked.connect(get_in_file)
out_dir.clicked.connect(get_out_dir)
button.clicked.connect(run_app)

w.show()
app.exec_()