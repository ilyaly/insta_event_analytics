import requests
import time
import csv

#This script collects a list of users who have a posts with given hashtag

post_url = 'https://www.instagram.com/p/'
payload = {'__a': '1'}

#Set hashtag and path for output here

hashtag = input('Enter hashtag to look for posts: ')
output = input('Enter the directory for output: ')
output_file = output +  hashtag + '_users.csv'
output_temp_file = output + hashtag + '_users_temporary.csv'

def save_list_as_scv(output_path,list):
    print('Saving to csv')
    with open(output_path, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in list:
            writer.writerow([val])
    print('Saving to csv has been finished!')


def get_usernames(url):
    print('Process started')
    user_names = []
    try:
        page = requests.get(url,params=payload).json()['graphql']['hashtag']['edge_hashtag_to_media']['edges']
        for p in page:
            shortcode = p['node']['shortcode']
            user_name = requests.get(post_url + shortcode, params=payload).json()['graphql']['shortcode_media']['owner']['username']
            print(user_name)
            user_names.append(user_name)
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
    user_names = list(set(user_names))
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
    for i in range(1):
    #while cursor is not None:
        try:
            res_next = requests.get(page_url, params=payload).json() #getting an instagram page info as json
            cursor = res_next['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor'] #getting maxid code to paginate
            if cursor is not None:
                page_url = "https://www.instagram.com/explore/tags/" + hashtag + "/?__a=1&max_id=" + cursor #getting next page
                pages_list.append(page_url)
                print('...')
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
    print('Collecting pages with taged post has been finished in ' + str(time.clock()))
    return pages_list

def all_users(pages_list):
    all_users = []
    for p in pages_list:
        users = get_usernames(p)
        all_users.append(users)
        save_list_as_scv(output_temp_file,all_users)
    return all_users

if __name__ == '__main__':
     user_names_list = []
     unique_users = []
     pages_list = get_taged_pages(hashtag)
     user_names_list = all_users(pages_list)
     for u_list in user_names_list:
         for us in u_list:
                 unique_users.append(us)
     print(unique_users)
     save_list_as_scv(output_file,unique_users)
