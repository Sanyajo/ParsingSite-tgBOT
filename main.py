import requests
from bs4 import BeautifulSoup
import threading
import json

lval = 100
rval = 115

def get_first_art():

    f = open('text.txt','w')

    headers ={
        "user-agent": "you user-agent"
    }
    url = f"https://www.kufar.by/l/r~brest/noutbuki?prc=r%3A{lval}00%2C{rval}00&sort=lst.d"
    r = requests.get(url = url, headers = headers)

    soup = BeautifulSoup(r.text, 'lxml')
    all_link = soup.find_all("a", class_="styles_wrapper__yaLfq")
    image_link = soup.find_all("img",class_="styles_image__eGgZr")

    new_dict = {}
    image_dict=[]

    for j in image_link:
        img = j.get("data-src")
        image_dict.append(img)

    k = 0
    for i in all_link:
        art_name = i.find("h3", class_= "styles_title__ARIVF").text.strip()
        art_link = i.get("href")
        art_id = art_link[26:35]
        art_cost = i.find("div",class_ = "styles_top__HNf3a").text.strip()
        art_city = i.find("div", class_ = "styles_secondary__NEYhw").text.strip()

        f.write(f"{art_name} \t| {art_link} \t| {art_cost} \t| {art_id}  \n")

        if(art_city == "Брест"):
            new_dict[art_id] = {
                "Название: ": art_name,
                "Ссылка: ": art_link,
                "Цена: ": art_cost,
                "Фото: ": image_dict[k]
            }
        else:
            continue
        k = k + 1

    with open("dataBase.json", "w") as file:
        json.dump(new_dict,file, indent = 4, ensure_ascii = False)

    return f"БД обновилась{k}"

def check_new_art():

    with open("dataBase.json") as file:
        new_dict = json.load(file)

    headers = {
        "user-agent": "you user-agent"
    }
    url = f"https://www.kufar.by/l/r~brest/noutbuki?prc=r%3A{lval}00%2C{rval}00&sort=lst.d"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    all_link = soup.find_all("a", class_="styles_wrapper__yaLfq")
    image_link = soup.find_all("img", class_="styles_image__eGgZr")

    fresh_dict = {}
    fresh_image_dict = []

    k=0

    for j in image_link:
        img = j.get("data-src")
        if img in new_dict:
            continue
        else:
            fresh_image_dict.append(img)
        k = k+1
    k = 0
    for i in all_link:
        art_link = i.get("href")
        art_id = art_link[26:35]
        art_city = i.find("div", class_="styles_secondary__NEYhw").text.strip()

        if art_id in new_dict:
            continue
        if art_city == "Брест":
            art_name = i.find("h3", class_="styles_title__ARIVF").text.strip()
            art_link = i.get("href")
            art_id = art_link[26:35]
            art_cost = i.find("div", class_="styles_top__HNf3a").text.strip()


            new_dict[art_id] = {
                "Название: ": art_name,
                "Ссылка: ": art_link,
                "Цена: ": art_cost,
                "Фото: ": fresh_image_dict[k]
            }

            fresh_dict[art_id] = {
                "Название: ": art_name,
                "Ссылка: ": art_link,
                "Цена: ": art_cost,
                "Фото: ": fresh_image_dict[k]
            }
        else:
            continue
        k = k + 1

            # print("Новая запись")

    with open("dataBase.json",'w') as file:
        json.dump(new_dict, file, indent=4, ensure_ascii=False)

    return fresh_dict

if __name__ == "__main__":
    print(get_first_art())
    # print(check_new_art())

