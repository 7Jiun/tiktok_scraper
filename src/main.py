import time
import random
import subprocess
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import psutil


def random_sleep(minimum, maximum):
    time.sleep(random.uniform(minimum, maximum))


def get_tiktok_video_stat(video_path):
    stats = {
        "like": 2222,
        "comments": 22,
        "share": 17
    }
    return stats


def is_port_in_use(port):
    return any(conn.laddr.port == port for conn in psutil.net_connections())


def start_chrome_subprocess(chrome_app_path, port, user_data_dir):
    if not is_port_in_use(port):
        p = subprocess.Popen([chrome_app_path,
                              f'--remote-debugging-port={port}',
                              f'--user-data-dir={user_data_dir}'])
    else:
        print(f'{port}已被使用。')


def start_chrome_driver(chrome_driver_path, port):
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option(
        "debuggerAddress", f'localhost:{port}')
    chrome_options.page_load_strategy = 'normal'

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def scrape_tiktok_user_videos(driver, tiktok_user):
    try:
        driver.get(f'https://www.tiktok.com/@{tiktok_user}')
        random_sleep(3, 5)
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        video_infos = []
        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            random_sleep(4, 6)

            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            current_page_html = driver.page_source
            soup = BeautifulSoup(current_page_html, 'html.parser')
            div_items = soup.find_all(
                'div', class_='css-x6y88p-DivItemContainerV2')
            for div_item in div_items:
                video_info = {
                    "video_title": '',
                    "video_link": '',
                    "viewed_number": ''
                }

                title_element = div_item.find('a', title=True)
                if title_element and 'title' in title_element.attrs:
                    video_info["video_title"] = title_element['title']

                link_element = div_item.find('a', href=True)
                if link_element and 'href' in link_element.attrs:
                    video_info["video_link"] = link_element['href']

                views_element = div_item.find(
                    'strong', attrs={'data-e2e': 'video-views'})

                if views_element:
                    video_info["viewed_number"] = views_element.text

                video_infos.append(video_info)
        return video_infos
    except Exception as e:
        print(f'scraping interruptted, error: {e}')
    finally:
        driver.quit()


# Example usage
chrome_driver_path = '/Users/wuqijun/Downloads/chromedriver-mac-arm64/chromedriver'
chrome_app_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
port = 3002
user_data_dir = '/Users/wuqijun/Library/Application Support/Google/Chrome/Default'
tiktok_user = 'geevideo'
start_chrome_subprocess(chrome_app_path, port, user_data_dir)
driver = start_chrome_driver(
    chrome_driver_path, port)
user_video_infos = scrape_tiktok_user_videos(driver, tiktok_user)
print(user_video_infos)
schema = {
    "video_link": "https://www.tiktok.com/@geevideo/video/7294480190065970450",
    "video_title": "即新聞快報",
    "viewed_number": 222,
    "liked_number": 20,
    "comment_number": 12,
    "saved_number": 6,
    "shared_number": 3
}
