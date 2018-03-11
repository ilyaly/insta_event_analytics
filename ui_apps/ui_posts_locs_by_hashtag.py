import PySide,requests,geojson,geocoder,csv,json,sys,time
from PySide import QtGui
from PySide import QtCore


app = QtGui.QApplication(sys.argv)
wind = QtGui.QMainWindow()
wind.resize(220,100)
wind.move(100,100)

tag_label = QtGui.QLabel('Enter hashtag to define posts locations',wind)
tag_label.resize(200,20)
tag_label.move(10,10)

tag = QtGui.QLineEdit(wind)
tag.resize(200,20)
tag.move(10,40)

dirct = QtGui.QPushButton('Select working directory..',wind)
dirct.resize(200,20)
dirct.move(10,70)

start = QtGui.QPushButton('Start process..',wind)
start.resize(200,20)
start.move(10,100)


output = ['']

def get_dir():
    direct = QtGui.QFileDialog.getExistingDirectory()
    output[0] = direct
    return direct

def star_process():
    hashtag = str(tag.text())
    post_url = 'https://www.instagram.com/p/'
    payload = {'__a': '1'}

    print('\n\n')

    # Set hashtag and path for output here


    number_of_pages_option = True


    output_file = output[0] + '\\' +  hashtag + '_users.csv'
    output_loc_file = output[0] + '\\' + hashtag + '_locations.csv'

    def save_list_as_scv(output_path, list):
        print('Saving to csv')
        with open(output_path, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            for val in list:
                writer.writerow([val])
        print('Saving to csv has been finished!')

    def get_posts_locs(url):
        print('Collecting usernames..')
        user_names = []
        post_locs = []
        try:
            page = requests.get(url, params=payload).json()['graphql']['hashtag']['edge_hashtag_to_media']['edges']
            for p in page:
                start_time = time.clock()
                shortcode = p['node']['shortcode']
                try:
                    user_name = requests.get(post_url + shortcode, params=payload).json()['graphql']['shortcode_media']['owner']['username']
                    post_loc = requests.get(post_url + shortcode, params=payload).json()['graphql']['shortcode_media']['location']['name']
                    print(user_name + '' + post_loc + ' processing time: ' + str(round(time.clock() - start_time, 2)))
                    user_names.append(user_name)
                    post_locs.append(post_loc)
                except:
                    pass
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh);
            time.sleep(10)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc);
            time.sleep(10)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt);
            time.sleep(10)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        return user_names,post_locs

    def get_taged_pages(hashtag):
        print('Collecting urls for tagged posts..')
        pages_list = []
        main_page_url = "https://www.instagram.com/explore/tags/%s/" % hashtag  # First page url
        pages_list.append(main_page_url)
        res = requests.get(main_page_url, params=payload).json()
        cursor = res['graphql']['hashtag']['edge_hashtag_to_media']['page_info'][
            'end_cursor']  # getting max id of the second page
        second_page = "https://www.instagram.com/explore/tags/" + hashtag + "/?__a=1&max_id=" + cursor
        pages_list.append(second_page)
        page_url = second_page
        if number_of_pages_option is True:
            while cursor is not None:
                try:
                    res_next = requests.get(page_url, params=payload).json()  # getting an instagram page info as json
                    cursor = res_next['graphql']['hashtag']['edge_hashtag_to_media']['page_info'][
                        'end_cursor']  # getting maxid code to paginate
                    if cursor is not None:
                        page_url = "https://www.instagram.com/explore/tags/" + hashtag + "/?__a=1&max_id=" + cursor  # getting next page
                        pages_list.append(page_url)
                        print('processing time...' + str(round(time.clock(), 2)) + " seconds")
                except requests.exceptions.HTTPError as errh:
                    print("Http Error:", errh);
                    time.sleep(10)
                except requests.exceptions.ConnectionError as errc:
                    print("Error Connecting:", errc);
                    time.sleep(10)
                except requests.exceptions.Timeout as errt:
                    print("Timeout Error:", errt);
                    time.sleep(10)
                except requests.exceptions.RequestException as err:
                    print("OOps: Something Else", err)
        else: pass
        return pages_list

    def all_users(pages_list):
        all_users = []
        all_locs = []
        for p in pages_list:
            if p is not None:
                users = get_posts_locs(p)[0]
                locs = get_posts_locs(p)[1]
                all_users.append(users)
                all_locs.append(locs)
            else:
                print('NoneType error..'); pass
        return all_users,all_locs

    def parse():
        user_names_list = []
        locations_list = []
        unique_users = []
        unique_locations = []
        pages_list = get_taged_pages(hashtag)
        user_names_list = all_users(pages_list)[0]
        locations_list = all_users(pages_list)[1]
        for u_list in user_names_list:
            for us in u_list:
                unique_users.append(us)
        save_list_as_scv(output_file, unique_users)
        for l_list in locations_list:
            for l in l_list:
                unique_locations.append(l)
        save_list_as_scv(output_loc_file, unique_locations)
        print('Processing has been finished!')
    parse()

dirct.clicked.connect(get_dir)
start.clicked.connect(star_process)
wind.show()
app.exec_()