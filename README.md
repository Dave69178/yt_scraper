# yt_scraper
Program for obtaining data from a YouTube channel

## Method

Standard webscraping approach using Selenium.
1. Navigate to desired channel
2. Load all videos and create list of URLs to scrape from
3. Extract data on each video
4. Load data into pandas DataFrame
5. Output as CSV

## Adblock

'extension_4_43_0_0.crx' is the .crx file for AdBlock which is added to the webdriver to maintain consistency throughout video webpages.

## Output

Currently the '.csv' file outputted will contain a dataframe consisting of the following columns:
 - 'link': URl of video
 - 'thumbnail': URL of thumbnail image
 - 'title': The title of the video
 - 'desc': The contents of the description
 - 'up_date': The upload date of the video
 - 'views': The number of views of the video
 - 'num_comments': The number of comments on a video

## Comments

The program will very easily be broken if changes are made to the webpages. Currently no fail-safes have been added.
