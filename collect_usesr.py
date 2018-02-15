#This script helps you to collect a list of users who have a posts with hashtag
from collections import Counter
import requests
import time
import csv
import multiprocessing

post_url = 'https://www.instagram.com/p/'
payload = {'__a': '1'}

#Define hashtag and path for output here

hashtag = ''
outputpath = ''

def save_list_as_scv(output_path,list):
    print('Saving to csv')
    with open(output_path, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in list:
            writer.writerow([val])
    print('Saving to csv has been finished!')


#Collects usernames from pages with hashtag
def get_usernames(url):
    print('Process started')
    user_names = []
    try:
        page = requests.get(url,params=payload).json()['graphql']['hashtag']['edge_hashtag_to_media']['edges']
        for p in page:
            shortcode = p['node']['shortcode']
            user_name = requests.get(post_url + shortcode, params=payload).json()['graphql']['shortcode_media']['owner']['username']
            #print(user_name)
            user_names.append(user_name)
    except: time.sleep(10) ; print('Excepion oqqured')
    user_names = list(set(user_names))
    #print('Number of unique users is :' + str(len(user_names)))
    #print('Finished in ' + str(time.clock()))
    return user_names

def get_taged_pages(hashtag):
    print('Collecting urls for tagged posts..')
    pages_list = []
    main_page_url = "https://www.instagram.com/explore/tags/%s/" % hashtag #First page url
    pages_list.append(main_page_url)
    res = requests.get(main_page_url, params=payload).json()
    cursor = res['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor'] #getting max id of the second page
    second_page = "https://www.instagram.com/explore/tags/" + hashtag + "/?__a=1&max_id=" + cursor
    pages_list.append(second_page)
    page_url = second_page
    while cursor is not None:
        try:
            res_next = requests.get(page_url, params=payload).json() #getting an instagram page info as json
            cursor = res_next['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor'] #getting maxid code to paginate
            if cursor is not None:
                page_url = "https://www.instagram.com/explore/tags/" + hashtag + "/?__a=1&max_id=" + cursor #getting next page
                pages_list.append(page_url)
        except: raise ;print('You have got an exeception!')
    print('Collecting taget post has been finished in ' + str(time.clock()))
    return pages_list

def us(pages_list):
    all_users = []
    for p in pages_list:
        users = get_usernames(p)
        all_users.append(users)
    return all_users

def get_user_pages(user_name):
    print('Collecting urls for tagged posts..')
    number_of_pages = 2
    pages_list = []
    main_page_url = "https://www.instagram.com/%s/" % user_name #First page url
    pages_list.append(main_page_url)
    try:
        res = requests.get(main_page_url, params=payload).json()
        cursor = res['user']['media']['page_info']['end_cursor'] #getting max id of the second page
        second_page = "https://www.instagram.com/" + user_name + "/?__a=1&max_id=" + cursor
        pages_list.append(second_page)
        page_url = second_page
        for i in range(number_of_pages):
            try:
                res_next = requests.get(page_url, params=payload).json() #getting an instagram page info as json
                cursor = res_next['user']['media']['page_info']['end_cursor'] #getting maxid code to paginate
                if cursor is not None:
                    page_url = "https://www.instagram.com/" + user_name + "/?__a=1&max_id=" + cursor #getting next page
                    pages_list.append(page_url)
            except: raise ;print('You have got an exeception!')
        print('Collecting taget post has been finished in ' + str(time.clock()))
    except: time.sleep(5)
    return pages_list

def get_user_home(user_name):
    pages_list = get_user_pages(user_name)
    user_loc_list = []
    for page in pages_list:
        try:
            res = requests.get(page,params=payload).json()['user']
        except: raise
        for r in res['media']['nodes']:
            link = 'https://www.instagram.com/p/' + r['code'] + '/'
            try:
                resq = requests.get(link, params=payload).json()
            except: raise
            try:
                a = resq['graphql']['shortcode_media']['location']['name']
                user_loc_list.append(a)
            except:
                time.sleep(1)
    loc_c = Counter(user_loc_list)
    user_home = loc_c.most_common(1)[0]
    print(user_home)
    return user_home

def final_processing(user_names_list):
    users_homes_locations = []
    for user in user_names_list:
        home = get_user_home(user)
        users_homes_locations.append(home)
        print('We have got a location!')
    return users_homes_locations




if __name__ == '__main__':
    users = []
    with open('D://users.csv', 'r') as f:
        reader = csv.reader(f)
        pages_list = list(reader)
    for p in pages_list:
        user = p[0]
        users.append(user)
    pool = multiprocessing.Pool(processes=10)
    user_homes = pool.map(final_processing,users)

    save_list_as_scv('D://homes.scv',user_homes)



if __name__ == '__main__':
     user_names_list = []
     unique_users = []
     pages_list = get_taged_pages(hashtag)
     pool = multiprocessing.Pool(processes=10)
     user_names_list = pool.map(us,pages_list)
     for u_list in user_names_list:
         for us in u_list:
             for u in us:
                 print(u)
                 unique_users.append(u)
     print(unique_users)
     save_list_as_scv(outputpath,unique_users)
