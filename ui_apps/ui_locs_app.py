from collections import Counter
import requests,sys,time,csv,json
import geocoder
from PySide.QtGui import *
from PySide import QtGui
#This script collects a list with homes loactions of given users

payload = {'__a': '1'}
user_pagination_sufix = '?__a=1&max_id='





#users_csv = input('Enter the path to CSV with user names : \n')

geocoding_option = True


app = QApplication(sys.argv)
w = QWidget()
w.setWindowTitle('Insta event analytics')
w.setWindowIcon(QtGui.QIcon('C:\\Users\\Admin\\Desktop\\insta.jpg'))
w.resize(440, 150)

info = QLabel('Выберите *.csv с пользователям и задайте путь сохранения, нажмите "Искать пользователей"\nЗа процессом можно следить в консоли.',w)
info.resize(420,40)
info.move(20,10)

# Create textbox
in_dir = QPushButton('Выберить *.csv с пользователям',w)
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
    output = dirlist[0]
    # output.replace('\\','\\\\')
    users_csv = filelist[0]
    output_file = output + 'homes.csv'
    output_file_geo = output + '_homes_geo.csv'

    def save_list_as_scv(output_path,list,encoding='utf-8'):
        with open(output_path, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            for val in list:
                try:
                    writer.writerow([val])
                except UnicodeEncodeError as err:
                    print('Decoding this shit' + str(err))
                    try:
                        val = val.encode('cp1251').decode('utf-8')
                        writer.writerow([val])
                    except: pass ; writer.writerow(['undefined'])


    def open_csv_as_list(path_to_csv):
        users = []
        with open(path_to_csv, 'r') as f:
            reader = csv.reader(f)
            pages_list = list(reader)
        for p in pages_list:
            user = p[0]
            users.append(user)
        return users

    def get_post_urls_from_page(response):
        posts_urls = []
        res_user = response
        for r in res_user['user']['media']['nodes']:
            url = 'https://www.instagram.com/p/' + r['code'] + '/'
            posts_urls.append(url)
        return posts_urls

    def get_user_posts_urls(username,number_of_pages=5):
        posts_urls = []
        main_page_url = "https://www.instagram.com/%s/" % username
        try:
            respose = requests.get(main_page_url,params=payload).json()
            posts_urls.append(get_post_urls_from_page(respose))
            cursor = respose['user']['media']['page_info']['end_cursor']
            try:
                second_page = main_page_url + user_pagination_sufix + cursor
                next_page_url = second_page
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh) ; time.sleep(10)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc) ; time.sleep(10)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt) ; time.sleep(10)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)

            for p in range(number_of_pages-1):
                try:
                    respose = requests.get(next_page_url, params=payload).json()
                    posts_urls.append(get_post_urls_from_page(respose))
                    cursor = respose['user']['media']['page_info']['end_cursor']
                    if cursor is not None:
                        next_page_url = main_page_url + user_pagination_sufix + cursor

                except requests.exceptions.HTTPError as errh:
                    print("Http Error:", errh); time.sleep(10)
                    time.sleep(10)
                except requests.exceptions.ConnectionError as errc:
                    print("Error Connecting:", errc); time.sleep(10)
                    time.sleep(10)
                except requests.exceptions.Timeout as errt:
                    print("Timeout Error:", errt); time.sleep(10)
                    time.sleep(10)
                except json.decoder.JSONDecodeError as jerr:
                    print('Json error', jerr)
                except requests.exceptions.RequestException as err:
                    print("OOps: Something Else 1", err)
        except : pass
        return posts_urls

    def get_user_home_location_from_posts(posts_urls):
        user_locations = []
        for urls in posts_urls:
            for url in urls:
                try:
                    response = requests.get(url, params=payload).json()
                    test = response['graphql']['shortcode_media']['location']
                    if test is not None:
                        location = response['graphql']['shortcode_media']['location']['name']
                        user_locations.append(location)
                except requests.exceptions.HTTPError as errh:
                    print("Http Error:", errh);
                    time.sleep(10)
                except requests.exceptions.ConnectionError as errc:
                    print("Error Connecting:", errc);
                    time.sleep(10)
                except requests.exceptions.Timeout as errt:
                    print("Timeout Error:", errt);
                    time.sleep(10)
                except json.decoder.JSONDecodeError as jerr:
                    print('Json error', jerr)
                    user_locations.append('notdefined')
                except requests.exceptions.RequestException as err:
                    print("OOps: Something Else 2", err)
        count_locations = Counter(user_locations)
        try:
            user_home_location = count_locations.most_common(1)[0][0]
        except IndexError as err:
            try:
                user_home_location = count_locations.most_common(1)[0]
                print(err)
            except IndexError as err:
                try:
                    user_home_location = count_locations.most_common(1)
                    print(err)
                except: user_home_location = 'not defined'


        print(str(user_home_location) + ', collected in ' + str(int(time.clock())) + ' seconds -' )
        return user_home_location

    def get_home_locations_for_users_list(users_list):
        print('Collecting home locations')
        users_home_locations_geo_list = []
        users_home_locations_list = []
        for user in users_list:
            posts_urls = get_user_posts_urls(user)
            home_location = get_user_home_location_from_posts(posts_urls)
            users_home_locations_list.append(home_location)
            save_list_as_scv(output_file, users_home_locations_list)
            if geocoding_option is True:
                user_home_geo = geocoder.arcgis(str(home_location)).latlng
                users_home_locations_geo_list.append(str(user_home_geo))
                save_list_as_scv(output_file_geo, users_home_locations_geo_list)
            else: pass

        return users_home_locations_list, users_home_locations_geo_list



    def parse_location():

        users = open_csv_as_list(users_csv)
        homes = get_home_locations_for_users_list(users)[0]
        geo = get_home_locations_for_users_list(users)[1]
        save_list_as_scv(output_file,homes)
        if geocoding_option is True:
            save_list_as_scv(output_file_geo,geo)
        else: pass
        print("Finished!")
    parse_location()

in_dir.clicked.connect(get_in_file)
out_dir.clicked.connect(get_out_dir)
button.clicked.connect(run_app)
w.show()
app.exec_()