![](/ui_apps/insta.jpg)
# Insta events analytics - Analyzes of tourist flows using Instagram data (Depricated because of Instagram API changes)
![](/docs/clust_map.jpg)
**What is it?**

This repository is a set of scripts for analyzing tourist flows based on user data in an instagram of people or other event.
The scripts are written for use in research devoted to event tourism to determine tourist flows.

** Are there any examples? **

An example of a result map can be found at: https://ilyaly.github.io/insta_event_analytics/index.html
This map represents tourist flows at the Wild Mint festival in 2017. The hashtag ** wildmaat2017 ** was used to search for visitors.

**How ​​it works?**

There are two scripts in the repository:
- collect_users
- collect_home_locations
- geocoder
- leaflet_map_creator

The collect_users script collects the names of users having Instagram posts with a specific hashtag and saves the list of names to the * .csv file.
To determine the tourist flows of the event, you must use the official or the most popular hashtag of the event.

The "collect_homes_locatios" script collects home locations (geotag) of users from the list and saves them to a * .csv file and a file with coordinates in * geojson

The script "geocoder" - a separate script for geocoding * .csv with geotagging home location

The script "leaflet_map_creator" creates an HTML page with a map of home locations

In the UI_apps directory there are scripts with a user interface. To run, we need PySide.

** Scripts with interface **

Follow the link: https://github.com/ilyaly/insta_event_analytics/releases,
Download files:
ui_locs_app.exe
ui_map_app.exe
ui_users_app.exe

Use simple UI scripts.


** The principle of the algorithms **

- 1. Script collects a list of links to all posts with a given hashtag.
- 2. Makes a request to the page of each post from the list and gets the user name. Duplicate values ​​are removed from the list of users.
- 3. Links to the last 48 posts are collected for each user (the quantity can be changed, selected for an acceptable processing time with an acceptable accuracy in determining the home location).
- 4. A request is made to the page of each post and the geo-location of the post is collected.
- 5. A list of user geo-positions is compiled and the most frequently occurring is selected.
- 6. This location is considered home and is added to the list of home locations

**How ​​to use?**

Run the desired script and follow the instructions in the Python console.
Or download * .exe files from https://github.com/ilyaly/insta_event_analytics/releases link and work through the interface.


** Dependencies **

Python 3,
Libs: geocoder.py, geojson.py
For scripts with UI - PySide.
