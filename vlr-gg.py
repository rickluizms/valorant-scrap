import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options
import json

# Get content
url = "https://www.vlr.gg/stats/?event_group_id=45&event_id=all&region=all&country=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all"

option = Options()
option.add_argument("--headless=new")
driver = webdriver.Firefox()

driver.get(url)
time.sleep(1)

element = driver.find_element("xpath", "//div[@class='wf-card mod-table mod-dark']//table[@class='wf-table mod-stats mod-scroll']")
html_content = element.get_attribute('outerHTML')

# Parser HTML content
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

# Make a dataframe
df_full = pd.read_html(str(table))[0]
df = df_full[['Player', 'Agents', 'Rnd', 'R',  'ACS', 'K:D', 'KAST', 'ADR', 'KPR', 'APR', 'FKPR', 'FDPR', 'HS%', 'CL%', 'CL', 'KMax', 'K', 'D', 'A', 'FK', 'FD']]
df.columns = ['Player', 'Agents', 'Rnd', 'R',  'ACS', 'K:D', 'KAST', 'ADR', 'KPR', 'APR', 'FKPR', 'FDPR', 'HS%', 'CL%', 'CL', 'KMax', 'K', 'D', 'A', 'FK', 'FD']

print(df)
# Transform data in a dict
ranking = {}
ranking = df.to_dict('records')

driver.quit()
# Convert and save as JSON
js = json.dumps(ranking)
fp = open('ranking.json', 'w')
fp.write(js)
fp.close()
