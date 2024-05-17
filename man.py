import os
import ssl
import requests
import urllib.request
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import random

# 这个脚本是采集百度图片，只需要输入关键字，就会爬取百度图片
query = "毛坯房"

# 禁用不安全请求的警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 发送请求并禁用 SSL 证书验证
# response = requests.get('https://img0.baidu.com', verify=False)


size = 30

def fetch_image_urls(query, current_page):
    global size
    pn = current_page * size
    gsm = hex(pn)[2:]  # 切片去除前缀"0x"
    # 1715766715056
    current_timestamp_ms = int(time.time() * 1000)
    random_milliseconds = random.randint(1, 100000)
    ts = current_timestamp_ms + random_milliseconds

    # url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&logid=10823400497212599350&ipn=rj&ct=201326592&is=&fp=result&fr=ala&word=%E5%AE%A4%E5%86%85%E8%AE%BE%E8%AE%A1%E6%95%88%E6%9E%9C%E5%9B%BE&queryWord=%E5%AE%A4%E5%86%85%E8%AE%BE%E8%AE%A1%E6%95%88%E6%9E%9C%E5%9B%BE&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&expermode=&nojc=&isAsync=&pn={pn}&rn=30&gsm={gsm}&{new_timestamp_ms}="
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    # }
    # response = requests.get(url, headers=headers, verify=False)
    # if response.status_code == 200:
    #     # Parse the response JSON if the data is returned in JSON format
    #     # For now, let's assume it's a JSON response
    #     data = response.json()['data']
    #     img_urls = [item['middleURL'] for item in data if 'middleURL' in item]
    #     return img_urls
    # else:
    #     print("Failed to fetch images.")
    #     return []

    url = "https://image.baidu.com/search/acjson"

    params = {
        "tn": "resultjson_com",
        "logid": "11682988955955788781",
        "ipn": "rj",
        "ct": "201326592",
        "is": "",
        "fp": "result",
        "fr": "",
        "word": f"{query}",
        "queryWord": f"{query}",
        "cl": "2",
        "lm": "-1",
        "ie": "utf-8",
        "oe": "utf-8",
        "adpicid": "",
        "st": "-1",
        "z": "",
        "ic": "",
        "hd": "",
        "latest": "",
        "copyright": "",
        "s": "",
        "se": "",
        "tab": "",
        "width": "",
        "height": "",
        "face": "0",
        "istype": "2",
        "qc": "",
        "nc": "1",
        "expermode": "",
        "nojc": "",
        "isAsync": "",
        "pn": f"{pn}",
        "rn": "30",
        "gsm": f"{gsm}",
        f"{ts}": ""
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }

    response = requests.get(url, params=params, headers=headers, verify=False)

    if response.status_code == 200:
        try:
            # Parse the response JSON if the data is returned in JSON format
            data = response.json().get('data', [])
            img_urls = [item['middleURL'] for item in data if 'middleURL' in item]
            return img_urls
        except ValueError:
            print("Response content is not in JSON format.")
    else:
        print("Failed to fetch images.")

def download_images(image_urls, current_page, query):
    global size
    dir = query
    if not os.path.exists(f"{dir}"):
        os.makedirs(f"{dir}")
    
    
    for i, url in enumerate(image_urls, 1):
        filename = f"{dir}/image_{current_page * size + i}.jpg"
        response = requests.get(url, verify=False)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")

if __name__ == "__main__":
    current_page = 0
    max_pages = 100  # Change this to the maximum number of pages you want to fetch
    while current_page < max_pages:
        image_urls = fetch_image_urls(query, current_page)
        if not image_urls:
            print("No more images found. Exiting...")
            break
        download_images(image_urls, current_page, query)
        current_page += 1
