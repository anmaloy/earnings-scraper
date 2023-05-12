from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time

ticker = input('Ticker: ')
print(f'Downloading {ticker}')

# Loads the webdriver
options = Options()
options.add_argument('--headless')
page = f"https://www.zacks.com/stock/research/{ticker}/earnings-calendar"
driver = webdriver.Chrome(options=options)
driver.get(page)

# Selects from the dropdown, maximum of 100, or 25 years
try:
    x = driver.find_element('name', 'earnings_announcements_earnings_table_length')
    drop = Select(x)
    drop.select_by_visible_text("100")
    time.sleep(2)
except NoSuchElementException:
    print('\tTable not found: skipping')
    time.sleep(2)

# Extracts the html
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.close()

# Saves the table as a dataframe
table = pd.read_html(str(soup.find(id='earnings_announcements_earnings_table')))[0]

# Exports dataframe to csv
table.to_csv(f'{ticker}_earnings.csv', index=False)
print('\tDownloaded')
