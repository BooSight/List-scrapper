from bs4 import BeautifulSoup
from selenium import webdriver
from gettext import find
import requests
import time
from wsgiref import headers
from pickle import GLOBAL
result_list=[]
# page_num=""


headers = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}


def get_source_html(url):
    driver = webdriver.Chrome(
        executable_path="/home/armen/Desktop/List.am-scrapper/chromedriver/chromedriver"
    )
    
    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(2)
        with open("src/source-page.html", "w") as file:
            file.write(driver.page_source)

    except Exception as _ex:
        print(_ex)

    finally:
        driver.close()
        driver.quit()


def get_items_urls(file_path):
    with open(file_path) as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("div", class_="gl")

    urls = []
    for item in items_divs:
        item_url = item.find_all("a")
        for url_href in item_url:
            x = url_href.get("href")
            urls.append(x)
    
    with open("src/items_urls.txt", "w") as file:
        for url in urls:
            items_urls = f"https://www.list.am{url}\n"
            file.write(items_urls)
    

def get_data(file_path):
    with open(file_path) as file:

        # url_list = file.readlines()
        # clear_url_list = []
        # for url in url_list:
        #     url = url.strip()
        #     clear_url_list.append(url)
        # print(clear_url_list)
        ########_or_next_string_########
        urls_list = [url.strip() for url in file.readlines()]
             
    i = 0
    for url in urls_list:
                
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        
        try:
            name_surname = soup.find("a", class_="n").find("div").text.strip()
        except Exception as _ex:
            name_surname = None
        
        try:
            wanted_urls = soup.find("span", class_="clabel").text.strip()
            if wanted_urls == "Wanted":
                continue
        except Exception as _ex:
            wanted_urls = None

        try:
            item_name = soup.find("h1", {"itemprop": "name"}).text.strip()
        except Exception as _ex:
            item_name = None

        try:
            item_price = soup.find("span", class_="price").get("content").strip()
        except Exception as _ex:
            item_price = None

        try:
            item_currency = soup.find("meta", {"itemprop": "priceCurrency"}).get("content").strip()
        except Exception as _ex:
            item_currency = None

        try:
            item_price_period = soup.find("span", class_= "price").text.strip()
            result = item_price_period.find('daily')
            if result == -1:
                item_price_period = "Mounthly"
            else:
                item_price_period = "Daily"
        except Exception as _ex:
            item_price_period = None

        try:
            item_location = soup.find("div", class_="loc").find("a").text.strip()
        except Exception as _ex:
            item_location = None
        
        # try:
        #     page_num = soup1.find_all("div", {"id":"contentr"})
        #     print(page_num)
        # except Exception as _ex:
        #     page_num = None
        # print(page_num)

        result_list.append(f"{item_name}?{item_price}?{item_currency}?{item_price_period}?{item_location}?{name_surname}?{url}\n")
        
        i+=1
        print(i)
    

def parse_run(URL, LOC, MIN, MAX, pages):    
    
    global result_list
    # global page_num
        
    i = 1
    while (i <= pages):
        URL1 = f"{URL}"+str(i)+f"?n={LOC}&price1={MIN}&price2={MAX}"
        print(URL1)

        get_source_html(url=URL1)
        print("done")
        get_items_urls(file_path="/home/armen/Desktop/List.am-scrapper/src/source-page.html")
        print("done")
        get_data(file_path="/home/armen/Desktop/List.am-scrapper/src/items_urls.txt")
        print("done")

        i=i+1
     
    with open("src/list.ods", "w") as file:
        head = f"Name?Price?Currency?Price_period?Location?Name_Surname?url\n"
        file.write(head)
        for aaa in result_list:
            file.write(aaa)


