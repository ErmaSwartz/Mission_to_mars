#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd 
import requests
import time 
import pymongo


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# In[3]:


# 1. Use browser to visit the URL 
d1_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(d1_url)


# In[4]:


# Visit the weather website
url_weather = "https://mars.nasa.gov/insight/weather/"
browser.visit(url_weather)
# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[5]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
#search for elements with specific combo 
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# # visit the nasa mars news site 
# 

# In[6]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[7]:


slide_elem


# In[8]:


# assign the title and summary text to variables 
slide_elem.find("div", class_='content_title')


# In[9]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[10]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images 

# In[11]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[12]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[13]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[14]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[15]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[16]:


# Find the relative image url
# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url
# an img tag is nested within this html so weve included it 
# .get('src') pull the link to the image 


# In[17]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[18]:


# convert dataframe back into html 
df.to_html


# In[19]:


#end the session
browser.quit()


# # Mars Facts 
# 

# In[20]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[21]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[22]:


df.to_html()


# # Mars Weather 
# 

# In[23]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1 Scrape High-Res photos and titles 

# In[24]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# In[25]:


# # 1. Use browser to visit the URL 
d1_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(d1_url)


# In[26]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
hempisphere_dictionary = {}
# 3. Write code to retrieve the image urls and titles for each hemisphere.


# Parse the HTML
html = browser.html
html_soup = soup(html, 'html.parser')


# In[27]:


nasa = browser.find_by_tag('h3')


# In[28]:


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


# In[29]:


hempisphere_dictionary


# In[30]:


# add the dictionary to the list 
hemisphere_image_urls.append(hempisphere_dictionary)


# In[31]:


img_url = f'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/image/featured/mars2.jpg'
img_url


# In[32]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[ ]:


# 5. Quit the browser
browser.quit()

