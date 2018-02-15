from collections import Counter
import requests
import time
import csv
import json
import multiprocessing

#This script collects a list with homes loactions of given users

payload = {'__a': '1'}
user_pagination_sufix = '?__a=1&max_id='

#Set the path to input scv with user and output here

users_csv = ''
output = ''

def save_list_as_scv(output_path,list,encoding='utf-8'):
    print('Saving to csv')
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


    print('Saving to csv has been finished!')

def open_csv_as_list(path_to_csv):
    users = []
    with open('D://users.csv', 'r') as f:
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
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else 1", err)

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


    print('User_home_collected..' + str(time.clock()) + ' ' + str(user_home_location))
    return user_home_location

def get_home_locations_for_users_list(users_list):
    users_home_locations_list = []
    for user in users_list:
        posts_urls = get_user_posts_urls(user)
        home_location = get_user_home_location_from_posts(posts_urls)
        users_home_locations_list.append(home_location)
        save_list_as_scv('D://temp_homes.csv',users_home_locations_list)
        print(users_home_locations_list)
    return users_home_locations_list



if __name__ == '__main__':
    users = open_csv_as_list(users_csv)
    #pool = multiprocessing.Pool(processes=10)
    #homes = pool.map(get_home_locations_for_users_list,users)
    homes = get_home_locations_for_users_list(users)

    save_list_as_scv(outputpath,homes)