# Tiktok scraper

This project leverages a web driver to implement an automated TikTok user video data crawler. It is designed to scrape information such as video titles, links, view counts, likes, comments, shares, saves, and recording times for specified users in specific time period (must more than a week).

## Features

    - Data Scraping: Automates the scraping of video information from TikTok users.
    - Scheduled Tasks: Supports scheduled data scraping to track changes in video stats.
    - Data Updating: Identifies new videos and updates existing video data.
    - Data Storage: Saves scraped data into CSV files.

## Environment Requirements

    - Python 3.x
    - BeautifulSoup
    - Selenium
    - Chromedriver
    - Chrome browser
    - psutil
    - python-dotenv

## Installation Guide

    1. Install python packages:
        pip install beautifulsoup4 selenium psutil python-dotenv
    2. Download Chromedriver:
        first, check your chrome version by enter URL: 'chrome://version',
        then, go to [chrome_driver_homepage](https://chromedriver.chromium.org/downloads/version-selection) and download the version meet your chrome browser

## Usage

    1. Set up Environment Variables:
        - CHROME_DRIVER_PATH: Path to your Chromedriver.
        - CHROME_APP_PATH: Path to your Chrome application.
        - PORT: Port for remote debugging.
        - USER_DATA_DIR: Path to the user data of Chrome. (you can get yours in 'chrome://version')
        - TIKTOK_USER: Target TikTok username.
        - DEADLINE_TIME: The last date of the data you want to track, please follow the format '{Month}-{Day}'; examples:'3-15','12-5','11-16','1-9'
        - CRAWLER_PERIOD: the work cycle for the program. enter 1 for track every hour.
        - CSV_DIR: the route of scraped data

    2. start crawler by following command:
        sudo python src/main.py

    3. data will be save in the folder and in the .csv
