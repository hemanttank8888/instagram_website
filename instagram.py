import json
import random
import re
import time
import requests
import instaloader


data_list = []

def get_email(value):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(pattern, value)
    email = []
    if matches:
        email = [data for data in matches]
    return list(set(email))



def get_phone_number(value):
    data = re.findall(r'\+?\(?\d{1,3}\)?[0-9 .-]{8,}[0-9]', value)
    phone_number = []
    if data:
        phone_number = [data for data in data]
    return list(set(phone_number))

def send_request(username):

    proxies=[]
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    payload = {}
    headers = {
        'authority': 'www.instagram.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'x-ig-app-id': '936619743392459',
        'Cookie': 'csrftoken=m0nYjeNZLBiEB8HsDzPrcELAOHV5qU18; ds_user_id=64148896210; ig_did=C055E2A3-950B-4CEA-8366-7EE769121118; mid=ZZTrzAAEAAFbhufQFDzkCz6u9fCz; rur="LDC\\05464148896210\\0541735360039:01f70153c5315382489176e24fdbce3bed597c2af41b35d8e3d0f4026b9645db98100d4e"'
    }
    print(username, "user name is >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    signal = True
    try:
        response = requests.request("GET", url, headers=headers, data=payload,proxies=random.choice(proxies),verify=True)
        signal = False
    except:
        pass
    if signal:
        try:
            response = requests.request("GET", url, headers=headers, data=payload,proxies=random.choice(proxies),verify=False)
        except:
            pass
    try:
        if "application/json" in response.headers.get("Content-Type", ""):
            json_object = json.loads(response.text)
            get_data = json_object.get('data', {}).get('user')
            if get_data is not None:
                if get_data.get('username') is not None:
                    with open("user_data.json", "w") as json_file:
                        json.dump(get_data, json_file)
                    data_dict = {
                        "user_name": get_data['username'],
                        "biography_mentions": get_data['biography'],
                        "full_name": get_data['full_name'],
                        "business_category_name": get_data['category_name'],
                        "followees": get_data['edge_follow']['count'],
                        "followers": get_data['edge_followed_by']['count'],
                        "email" : get_email(get_data['biography']),
                        "phone_number" : get_phone_number(get_data['biography'])
                    }
                    data_list.append(data_dict)
                    with open("kids_profile_details2.json", "w") as json_file:
                        json.dump(data_list, json_file)
    except:
        pass

def insta_login(username, password):
    L = instaloader.Instaloader()
    L.login(username, password)
    profile = instaloader.Profile.from_username(L.context, "Deltaworldcharter")
    following_username_list = []

    try:
        count = 0
        for followee in profile.get_followers():
            time.sleep(0.3)
            if followee.username not in following_username_list:
                print(followee.username)
                print(count)
                following_username_list.append(followee.username)
            count = count + 1
    except:
        pass
    return following_username_list

username = "patil@yopmail.com"
password = "PATILp@123"

following_username_list = insta_login(username, password)
with open("jet2.json", "w") as json_file:
    json.dump(following_username_list, json_file)

for username in following_username_list:
    send_request(username)