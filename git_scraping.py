# I read the following story by The Washington Post about a surge in cases in ICE detention centers in the U.S. I did a Google search and found that ICE publicly releases how many people are currently positive for Covid, how many have died, and how many have had Covid at one point.
# https: // www.washingtonpost.com/national-security/2022/02/01/covid-migrants-ice-detention/

# Value of this data set:
# As a group that is more vulnerable than the rest of the population and often lacks the resources to file complaints or lawsuits, I thought it would be worth looking at how many people in ICE detention centers are testing positive, and create a visualization that updates in real time.


# import libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np
import selenium
import csv
from datetime import date
import time

# selenium options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# selenium settings
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")


def get_data():
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=chrome_options
    )
    driver.get(
        "https://www.ice.gov/coronavirus#citations")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", {"caseStatus table table-bordered"})

    list_of_rows = []
    for row in table.find_all('tr'):
        list_of_cells = []
        for cell in row.find_all('td'):
            if cell.find('a'):
                list_of_cells.append(cell.find('a')['href'])
            text = cell.text.strip()
            list_of_cells.append(text)
        list_of_rows.append(list_of_cells)

    data = pd.DataFrame(list_of_rows, columns=[
                        "office_region", "current_confirmed_cases", "confirmed_deaths", "total_confirmed_cases"])
    # take out bigger office names
    today = date.today()
    data.to_csv(f"data/ice_covid/data_{today}.csv", index=False)
    with open(f'logs/log_record_{time.strftime("%Y%m%d-%H%M%S")}.txt', "w") as f:
        f.write(
            f'Scraper ran on {time.strftime("%Y%m%d-%H%M%S")}')


get_data()
