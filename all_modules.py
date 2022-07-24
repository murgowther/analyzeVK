from cgitb import text
import json
import os
import time
from typing import Text

import requests
from auth_data import token

# group_name = input("Введите название группы: ")
#
# url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=40&access_token={token}&v=5.52"
# req = requests.get(url)
# print(req.text)

def get_wall_posts(group_name):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=40&access_token={token}&v=5.103"
    req = requests.get(url)
    src = req.json()

    # проверяем существует ли директория с именем группы
    if os.path.exists(f"{group_name}"):
        print(f"Директория с именем {group_name} уже существует!")
    else:
        os.mkdir(group_name)

    # сохраняем данные в json файл, чтобы видеть структуру
    with open(f"{group_name}/{group_name}.json", "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    # собираем ID новых постов в список
    fresh_posts_id = []
    posts = src["response"]["items"]

    for fresh_post_id in posts:
        fresh_post_id = fresh_post_id["id"]
        fresh_posts_id.append(fresh_post_id)

    #cобираем комментарии - теперь в другом месте
    #all_commits = []
    #commits = src["response"]["items"]
    #for all_commit in commits:
     #   all_commit = all_commit["text"]
      #  all_commits.append(all_commit)

    """Проверка, если файла не существует, значит это первый
    парсинг группы(отправляем все новые посты). Иначе начинаем
    проверку и отправляем только новые посты."""
    if not os.path.exists(f"{group_name}/exist_posts_{group_name}.txt"):
        print("Файла с ID постов не существует, создаём файл!")

        with open(f"{group_name}/exist_posts_{group_name}.txt", "w") as file:
            for item in fresh_posts_id:
                file.write(str(item) + "\n")
        
        #with open(f"{group_name}/text_{group_name}.txt", "w") as file:
         #   for item in commits:
          #      file.write(str(item) + "\n")

        #post_str = post["text"]
        #print(f"{post_str}")
        # извлекаем данные из постов
        for post in posts:

            post_id = post["id"]
            print(f"Отправляем пост с ID {post_id}")
            


            try:
                if "attachments" in post:
                    post = post["attachments"]

                    # забираем фото
                    if post[0]["type"] == "photo":

                        photo_quality = [
                            "photo_2560",
                            "photo_1280",
                            "photo_807",
                            "photo_604",
                            "photo_130",
                            "photo_75"
                        ]

                        if len(post) == 1:

                            for pq in photo_quality:
                                if pq in post[0]["photo"]:
                                    post_photo = post[0]["photo"][pq]
                                    print(f"Фото с расширением {pq}")
                                    print(post_photo)
                                    break
                        else:
                            for post_item_photo in post:
                                if post_item_photo["type"] == "photo":
                                    for pq in photo_quality:
                                        if pq in post_item_photo["photo"]:
                                            post_photo = post_item_photo["photo"][pq]
                                            print(f"Фото с расширением {pq}")
                                            print(post_photo)
                                            break
                                else:
                                    print("Линк или аудио пост")
                                    break

            except Exception:
                print(f"Что-то пошло не так с постом ID {post_id}!")

    else:
        print("Файл с ID постов найден, начинаем выборку свежих постов!")

def check_list_and_comment(group_name,user_ids):
    l = []
    with open(f"{group_name}/exist_posts_{group_name}.txt") as f:
        l = f.read().splitlines()
    
    url = f"https://api.vk.com/method/wall.getComments?owner_id={user_ids}&post_id={l}&v=5.103"
    req = requests.get(url)
    src = req.json()
    with open(f"comment.json", "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)


def get_Profile_Info(group_name):
    url = f"https://api.vk.com/method/users.get?user_ids={group_name}&fields=activities,about,books,bdate,career,common_count,connections,contacts,city,country,domain,education,exports,followers_count,friend_status,home_town,sex,site,schools,screen_name,status,verified,games,interests,is_favorite,is_hidden_from_feed,last_seen,maiden_name,military,movies,music,nickname,occupation,online,personal,quotes,relation,relatives,timezone,tv,universities&access_token={token}&v=5.103"
    req = requests.get(url)
    src = req.json()

    if os.path.exists(f"{group_name}"):
        print(f"Директория с именем {group_name} уже существует!")
    else:
        os.mkdir(group_name)
    
    with open(f"{group_name}/info_user.json", "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)
    
    all_infos = []
    infos = src["response"]
    for all_info in infos:
        all_info = all_info["first_name"]
        all_infos.append(all_info)
    for all_info in infos:
        all_info = all_info["last_name"]
    all_infos.append(all_info)
    for all_info in infos:
        all_info = all_info["bdate"]
        all_infos.append(all_info)
    for all_info in infos:
        all_info = all_info["home_town"]
        all_infos.append(all_info)
    for all_info in infos:
        all_info = all_info["university_name"] 
        all_infos.append(all_info)
    for all_info in infos:
        all_info = all_info["faculty_name"] 
        all_infos.append(all_info)
    

    with open(f"{group_name}/main_Info_{group_name}.txt", "w", encoding='utf-8') as file:
            for item in all_infos:
                file.write(str(item) + "\n")


def get_gropus_info(group_name,user_ids):
    url = f"https://api.vk.com/method/groups.get?user_id={user_ids}&fields=photo_50&access_token={token}&extended=1&v=5.103"
    req = requests.get(url)
    src = req.json()

    if os.path.exists(f"{group_name}"):
        print(f"Директория с именем {group_name} уже существует!")
    else:
        os.mkdir(group_name)
    
    with open(f"{group_name}/groups_user.json", "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    all_commits = []
    commits = src["response"]["items"]
    for all_commit in commits:
        all_commit = all_commit["name"]
        all_commits.append(all_commit)

    """Проверка, если файла не существует, значит это первый
    парсинг группы(отправляем все новые посты). Иначе начинаем
    проверку и отправляем только новые посты."""
    with open(f"{group_name}/groups_{group_name}.txt", "w", encoding='utf-8') as file:
            for item in all_commits:
                file.write(str(item) + "\n")



def get_comments(group_name,user_ids):
    l = []
    with open(f"{group_name}/exist_posts_{group_name}.txt") as f:
        l = f.read().splitlines()
    for i in l:
        url = f"https://api.vk.com/method/wall.getComments?owner_id={user_ids}&post_id={i}&access_token={token}&v=5.103"
        req = requests.get(url)
        src = req.json()
        if os.path.exists(f"{group_name}"):
            print
        else:
            os.mkdir(group_name)
        with open(f"{group_name}/comment{i}.json", "w", encoding="utf-8") as file:
            json.dump(src, file, indent=4, ensure_ascii=False)
        time.sleep(1)
        
        all_commits = []
        commits = src["response"]["items"]
        for all_commit in commits:
            all_commit = all_commit["text"]
            all_commits.append(all_commit)

        """Проверка, если файла не существует, значит это первый
        парсинг группы(отправляем все новые посты). Иначе начинаем
        проверку и отправляем только новые посты."""
        with open(f"{group_name}/text_comment{i}_{group_name}.txt", "w", encoding='utf-8') as file:
                for item in all_commits:
                    file.write(str(item) + "\n")

    

def main(group_name, user_ids):
    get_wall_posts(group_name)
    check_list_and_comment(group_name,user_ids)
    get_Profile_Info(group_name)
    get_gropus_info(group_name,user_ids)
    get_comments(group_name,user_ids)


if __name__ == '__main__':
    main()
