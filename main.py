from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


# Function to wait until presence of element is located (type, path)
def presence_wait(locator, path):
    return wait.until(EC.presence_of_element_located((locator, path)))


# Setup AdBlock capability for chrome driver
chrop = webdriver.ChromeOptions()
chrop.add_extension('extension_4_43_0_0.crx')

# Obtain desired YouTube channel to scrape
yt_page = input("Enter the YouTube channel URL that you wish to scrape (copy/paste from browser, include 'https' etc):")

# Start chrome webdriver
driver = webdriver.Chrome("/usr/bin/chromedriver", options=chrop)
driver.implicitly_wait(10)  # Set implicit wait time of 10 seconds
wait = WebDriverWait(driver, 10)  # Object for explicit waits

# Go to YouTube page
driver.get(yt_page)
driver.maximize_window()

# Close extension install tab
driver.switch_to.window(driver.window_handles[1])
driver.close()
driver.switch_to.window(driver.window_handles[0])

# Locate button to agree to terms and continue to target page
agree_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#yDmH0d > c-wiz > div > div > div > "
                                                                       "div.NIoIEf > div.G4njw > div.qqtRac > form > "
                                                                       "div > div > button")))
agree_button.click()

# Locate "Videos" tab
video_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#tabsContent > tp-yt-paper-tab:nth-child(4)")))
video_tab.click()
time.sleep(1)

# Scroll down to load all videos
prev_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
while True:
    driver.execute_script("window.scrollBy(0,1000);")
    time.sleep(1)
    new_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
    if new_height == prev_height:
        break
    prev_height = new_height

# Get links for all videos
video_elements = driver.find_elements_by_id("video-title")
video_urls = [vid.get_attribute('href') for vid in video_elements]
print(len(video_urls))

# Setup list to store data to load into dataframe
data = []

# Loop through all videos and extract desired data
for video in video_urls:
    driver.get(video)
    link = video
    thumbnail = presence_wait(By.CSS_SELECTOR,"#watch7-content > link:nth-child(11)").get_attribute('href')
    title = presence_wait(By.CSS_SELECTOR,'#container > h1 > yt-formatted-string').text
    desc = presence_wait(By.CSS_SELECTOR,'#description > yt-formatted-string').get_attribute('innerHTML')
    up_date = presence_wait(By.CSS_SELECTOR, '#info-strings > yt-formatted-string').get_attribute('innerHTML')
    views = presence_wait(By.CSS_SELECTOR, '#count > ytd-video-view-count-renderer > '
                                           'span.view-count.style-scope.ytd-video-view-count-renderer').get_attribute('innerHTML')
    # Sleep for consistent scrolling of page (Scroll wouldn't execute properly if page not loaded sufficiently)
    time.sleep(0.25)
    # Scroll to load comment element
    driver.execute_script('window.scrollBy(0, 1000)')
    com_element = driver.find_element_by_css_selector('#count > yt-formatted-string > span:nth-child(1)')
    num_comments = com_element.get_attribute('innerHTML')

    data.append([link, thumbnail, title, desc, up_date, views, num_comments])

