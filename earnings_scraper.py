from bs4 import BeautifulSoup
import glob
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time

print('Earnings Download')

path = "data\\head\\*.csv"

for file in glob.glob(path):
    tickerList = pd.read_csv(file)
    for i in range(len(tickerList)):
        t = tickerList.iloc[i, 0]
        head, tail = os.path.split(file)
        name = os.path.splitext(tail)[0]
        print('Downloading ' + t + ' from ' + name)

        # Loads the webdriver
        options = Options()
        options.add_argument('--headless')
        page = f"https://www.zacks.com/stock/research/{t}/earnings-calendar"
        driver = webdriver.Chrome(options=options)
        driver.minimize_window()
        driver.get(page)

        # Selects from the dropdown, maximum of 100, or 25 years
        try:
            x = driver.find_element('name', 'earnings_announcements_earnings_table_length')
            drop = Select(x)
            drop.select_by_visible_text("100")
            time.sleep(2)
        except NoSuchElementException:
            print('\tTable not found: skipping')
            tickerList = tickerList.drop([i])
            time.sleep(2)
            continue

        # Extracts the html
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.close()

        # Saves the table as a dataframe
        table = pd.read_html(str(soup.find(id='earnings_announcements_earnings_table')))[0]

        # Exports dataframe to csv
        table.to_csv(f'data\\earnings\\{name}\\{t}.csv', index=False)
        print('\tDownloaded')
    tickerList.to_csv(file, index=False)
