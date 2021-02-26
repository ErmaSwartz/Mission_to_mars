# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd 
import requests
import time 
import pymongo


# %%
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# %%
# 1. Use browser to visit the URL 
d1_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(d1_url)


# %%
# Visit the weather website
url_weather = "https://mars.nasa.gov/insight/weather/"
browser.visit(url_weather)
# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# %%
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
#search for elements with specific combo 
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# %% [markdown]
# # visit the nasa mars news site 
# 

# %%
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# %%
slide_elem


# %%
# assign the title and summary text to variables 
slide_elem.find("div", class_='content_title')


# %%
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# %% [markdown]
# ### Featured Images 

# %%
# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# %%
# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# %%
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# %%
# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# %%
# Find the relative image url
# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url
# an img tag is nested within this html so weve included it 
# .get('src') pull the link to the image 


# %%
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# %%
# convert dataframe back into html 
df.to_html


# %%
#end the session
browser.quit()

# %% [markdown]
# # Mars Facts 
# 

# %%
df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# %%
df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# %%
df.to_html()

# %% [markdown]
# # Mars Weather 
# 

# %%
# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

# %% [markdown]
# # D1 Scrape High-Res photos and titles 

# %%
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# %%
# # 1. Use browser to visit the URL 
d1_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(d1_url)


# %%
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
hempisphere_dictionary = {}
# 3. Write code to retrieve the image urls and titles for each hemisphere.


# Parse the HTML
html = browser.html
html_soup = soup(html, 'html.parser')


# %%
nasa = browser.find_by_tag('h3')


# %%
results = html_soup.find_all('h3')

# loop over results to get article data
for result in results:
    result = result.get_text()
    browser.click_link_by_partial_text(result)
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # find the relative image url
    img_url = img_soup.find('img', class_='wide-image').get('src')
    title = img_soup.find('h2', class_='title').get_text()
    # add the title as key and images as value 
    hempisphere_dictionary[title] = img_url
    
    browser.back()


# %%
hempisphere_dictionary


# %%
# add the dictionary to the list 
hemisphere_image_urls.append(hempisphere_dictionary)


# %%
img_url = f'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/image/featured/mars2.jpg'
img_url


# %%
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# %%
# 5. Quit the browser
browser.quit()


