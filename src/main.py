import time
import random
import subprocess
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from write_csv import write_video_infos_into_csv, get_current_csv
from functools import partial
from dotenv import load_dotenv
import os
import psutil
import schedule


def random_sleep(minimum, maximum):
    time.sleep(random.uniform(minimum, maximum))


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
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
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
        counter = 1
        while (counter < 2):
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            random_sleep(5, 10)

            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            current_page_html = driver.page_source
            soup = BeautifulSoup(current_page_html, 'html.parser')
            div_items = soup.find_all(
                'div', class_='css-x6y88p-DivItemContainerV2')
            div_items_set = set(div_items)
            for div_item in div_items:
                video_info = {
                    "video_title": '',
                    "video_link": '',
                    "viewed_number": [0],
                    "likes_number": [0],
                    "comments_number": [0],
                    "saved_number": [0],
                    "shared_number": [0],
                    "record_time": [0],
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
                    video_info["viewed_number"][0] = views_element.text

                video_infos.append(video_info)
            counter += 1
        return video_infos
    except Exception as e:
        print(f'scraping interruptted, error: {e}')


def update_viewed_number(current_video_infos, new_scraped_user_infos):
    for current_video_info, new_scraped_user_info in zip(current_video_infos, new_scraped_user_infos):
        if 'viewed_number' not in current_video_info:
            current_video_info['viewed_number'] = []
        current_video_info['viewed_number'].append(
            new_scraped_user_info['viewed_number'][0])


def get_video_stat_data(soup, attribute_value):
    try:
        result = soup.find('strong', {'data-e2e': attribute_value}).text
        if result:
            return result
        else:
            print(f"No data found for {attribute_value}")
            return ''
    except AttributeError:
        print(f"Data extraction failed for {attribute_value}")
        return ''


def get_current_month_hour():
    now = datetime.now()
    month_and_hour = now.strftime("%m/%d %H:%M")
    return month_and_hour


def scrape_video_stats(driver, video_info):
    driver.get(video_info['video_link'])
    random_sleep(3, 5)  # 假設 random_sleep 是一個自定義函數
    current_page_html = driver.page_source
    soup = BeautifulSoup(current_page_html, 'html.parser')
    div_item = soup.find('div', class_='css-1npmxy5-DivActionItemContainer')
    attributes = ['like-count', 'comment-count',
                  'share-count', 'undefined-count']
    keys = ['likes_number', 'comments_number', 'shared_number', 'saved_number']

    for result_key, attribute in zip(keys, attributes):
        new_state_value = get_video_stat_data(div_item, attribute)
        if isinstance(video_info[result_key], list):
            video_info[result_key].append(new_state_value)
        else:
            video_info[result_key] = [new_state_value]

    current_month_and_hour = get_current_month_hour()
    if isinstance(video_info['record_time'], list):
        video_info['record_time'].append(current_month_and_hour)
    else:
        video_info['record_time'] = [current_month_and_hour]


def find_new_videos(current_video_infos, new_scraped_infos):
    current_video_links = {info['video_link'] for info in current_video_infos}
    new_videos = [
        info for info in new_scraped_infos if info['video_link'] not in current_video_links]

    return new_videos


def insert_new_videos_at_beginning(current_video_infos, new_videos):
    updated_video_infos = new_videos + current_video_infos
    return updated_video_infos


def close_driver(driver):
    driver.quit()


def full_scrape_job(status):
    load_dotenv()
    chrome_driver_path = os.getenv('CHROME_DRIVER_PATH')
    chrome_app_path = os.getenv('CHROME_APP_PATH')
    port = os.getenv('PORT')
    user_data_dir = os.getenv('USER_DATA_DIR')
    tiktok_user = os.getenv('TIKTOK_USER')
    csv_dir = f'../{tiktok_user}_video_stats.csv'

    start_chrome_subprocess(chrome_app_path, port, user_data_dir)
    driver = start_chrome_driver(
        chrome_driver_path, port)
    if status == 'first':
        user_video_infos = scrape_tiktok_user_videos(driver, tiktok_user)
        for video_info in user_video_infos:
            scrape_video_stats(driver, video_info)
        close_driver(driver)
        write_video_infos_into_csv(user_video_infos, csv_dir)
    elif status == 'track':
        user_video_infos = scrape_tiktok_user_videos(driver, tiktok_user)
        current_video_infos = get_current_csv(csv_dir)
        new_videos = find_new_videos(current_video_infos, user_video_infos)
        if (len(new_videos) > 0):
            current_video_infos = insert_new_videos_at_beginning(
                current_video_infos, new_videos)
        update_viewed_number(current_video_infos, user_video_infos)
        for video_info in current_video_infos:
            scrape_video_stats(driver, video_info)
        close_driver(driver)
        write_video_infos_into_csv(current_video_infos, csv_dir)
    else:
        print('invalid work status')


def safe_run(job_func):
    try:
        job_func()
    except Exception as e:
        current_time = get_current_month_hour()
        print(f"An error occurred: {e}, occured time:{current_time}")


try:
    full_scrape_job('first')
except Exception as e:
    print(f'first error: {e}')

schedule.every(1).hour.do(safe_run, partial(
    full_scrape_job, 'track'))
while True:
    schedule.run_pending()
    time.sleep(300)
