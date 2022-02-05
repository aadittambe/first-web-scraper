# import libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np
import selenium
import csv
from datetime import date


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
    data = data.replace(to_replace='None', value=np.nan).dropna()
    data.to_csv("tsa_data/main_log/log.csv", index=False)
    data.to_csv(f"tsa_data/log_daily/log_{today}.csv", index=False)


get_data()
