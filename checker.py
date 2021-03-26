import os
import json
import sys
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests

now = str(datetime.datetime.now())
print(f"\n{now}")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
  '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"'
)

raw_pages = os.getenv("WEBPAGES")
if raw_pages is None:
  print("Did not find environmental variable called \"WEBPAGES\"; will not check anything.")
  sys.exit(1)
ifttt_api_key = os.getenv("IFTTT_API_KEY")
if ifttt_api_key is None:
  print("Did not find environmental variable called \"IFTTT_API_KEY\" will not check anything.")
  sys.exit(1)

pages = json.loads(raw_pages)
something_available = False
driver = webdriver.Chrome(executable_path=os.path.abspath('/usr/bin/chromedriver'), chrome_options=chrome_options)
unloaded_pages = []
for page in pages:
  driver.set_page_load_timeout(15)
  try:
    driver.get(page['webpage'])
  except Exception as e:
    print(f"Couldn't get page ({page['item_name']}) because: {e}")
    unloaded_pages.append(page['item_name'])
    continue
  if page['text'] not in driver.find_element_by_tag_name('html').get_attribute('innerHTML'):
    requests.post(f'https://maker.ifttt.com/trigger/item_available/with/key/{ifttt_api_key}', {"value1": page['item_name'], "value2": page['webpage']})
    print(f"{page['item_name']} was available")
    print(driver.find_element_by_tag_name('html').get_attribute('innerHTML'))
    something_available = True
  else:
    print(f"Not available: {page['item_name']}")
  with open(f'/data/{page["item_name"].replace(" ", "_")}.txt', 'w') as f:
    f.write(driver.find_element_by_tag_name('html').text)
  driver.find_element_by_tag_name('html').screenshot(f'/data/{page["item_name"].replace(" ", "_")}.png')
driver.quit()
if not something_available:
  if os.getenv("ENABLE_NOT_IN_STOCK_NOTIFICATION") == 'true':
    requests.post(f'https://maker.ifttt.com/trigger/nothing_available/with/key/{ifttt_api_key}', {"value1": now, "value2": ','.join(unloaded_pages)})
  print("Nothing was available")
