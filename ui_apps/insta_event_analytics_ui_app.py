import PySide
import csv,geocoder,geojson,json,sys,webbrowser
from collections import Counter
from PySide.QtGui import *
from PySide import QtGui
import json.decoder

app = QApplication(sys.argv)
w = QMainWindow()
w.setWindowTitle('Instagram event analytics')
w.setWindowIcon(QtGui.QIcon('insta.jpg'))
w.resize(800, 260)

hashtag = QLabel('<b>Enter hahstag without #</b>',w)
hashtag.resize(200,15)
hashtag.move(10,10)

hashtag_field = QLineEdit(w)
hashtag_field.resize(200,20)
hashtag_field.move(10,30)

home_loc_threshold_label = QLabel('<b>Enter number of user post to define\nhome location: </b>',w)
home_loc_threshold_label.resize(200,25)
home_loc_threshold_label.move(10,60)
home_loc_threshold = QComboBox(w)
home_loc_threshold.resize(200,20)
home_loc_threshold.move(10,90)
home_loc_threshold.addItem('12')
home_loc_threshold.addItem('24')
home_loc_threshold.addItem('48')
home_loc_threshold.addItem('96')
home_loc_threshold.addItem('192')

map_type_label = QLabel('<b>Select map type: </b>',w)
map_type_label.resize(200,25)
map_type_label.move(10,115)
map_type = QComboBox(w)
map_type.resize(200,20)
map_type.move(10,145)
map_type.addItem('Regular')
map_type.addItem('Cluster-map')

working_dir = QPushButton('Select directory for outputs ',w)
working_dir.resize(200,25)
working_dir.move(10,180)

start_program = QPushButton('Start processing..',w)
start_program.resize(200,25)
start_program.move(10,220)


console_box_label = QLabel('<b>Current process log:</b>',w)
console_box_label.resize(200,20)
console_box_label.move(220,10)
console_box = QTextEdit('',w)
console_box.resize(570,215)
console_box.move(220,30)

vars = ['']



w.show()
app.exec_()