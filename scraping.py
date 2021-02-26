# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt 

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": scrape_hemisphere_data(browser),
        "last_modified": dt.datetime.now()
     }
    
     # Stop webdriver and return data
    browser.quit()
    return data
    
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def scrape_hemisphere_data(browser):
    d1_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(d1_url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.


    # Parse the HTML
    html = browser.html
    html_soup = soup(html, 'html.parser')
    # nasa = browser.find_by_tag('h3')
    results = html_soup.find_all('h3')

    # loop over results to get article data
    for result in results:
        hemisphere_dictionary = {}
        result = result.get_text()
        browser.click_link_by_partial_text(result)
        html = browser.html
        img_soup = soup(html, 'html.parser')
        # find the relative image url
        img_url = img_soup.find('img', class_='wide-image').get('src')
        full_url = 'https://astrogeology.usgs.gov' + img_url
        title = img_soup.find('h2', class_='title').get_text()
        # add the title as key and images as value 
        hemisphere_dictionary['img_url'] = full_url
        hemisphere_dictionary['title'] = title
        # add the dictionary to the list 
        hemisphere_image_urls.append(hemisphere_dictionary)
    
        browser.back()
    # add the dictionary to the list 
    
    return hemisphere_image_urls
browser.quit()