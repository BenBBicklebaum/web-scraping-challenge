#!/usr/bin/env python
# coding: utf-8

# In[57]:
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd

def scrape():

    # In[10]:


    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'


    # In[11]:


    # Retrieve page with the requests module
    response = requests.get(url)


    # In[12]: Begin Soup


    soup = BeautifulSoup(response.text, 'html.parser')


    # In[24]: Find the title nad description of the latest news


    titleresults = soup.find('div', class_='content_title').a.text.strip()
    descresults = soup.find('div', class_='rollover_description_inner').text.strip()
    

    # In[40]: begin the splinter setup


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)


    # In[41]: Go to the website with the featured image


    splinterlink = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(splinterlink)


    # In[42]: Go to the full image


    browser.click_link_by_id('full_image')


    # In[49]: find the URL for the full sized image & store it


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = "https://www.jpl.nasa.gov" + soup.find('a', class_='button fancybox')['data-fancybox-href']


    # In[55]: Go to the twitter site


    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    # In[56]: store the lates mars weather report tweet


    marstweet = soup.find_all('div', class_='js-tweet-text-container')[0].text.strip()


    # In[81]: go to the facts table wesbite, read the website, grab the first table, put in column names, set the index to Stats


    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    marstable_df = tables[0]
    marstable_df.columns = ['Stats', 'Values']
    marstable_df.set_index('Stats', inplace=True)

    # In[84]: convert the table to HTML and drop all \n values


    marstable_html = marstable_df.to_html()
    marstable_html = marstable_html.replace('\n', '')
    #or marstable_df.to_html(marstable.html)


    # In[104]: Go to the mars hemisphere website


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    marshemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(marshemi)
    souptitle = BeautifulSoup(response.text, 'html.parser')


    # In[105]: find all 4 hemispheres and store the title and image url in a dictionary


    hem = []
    hemisphere_image_urls = {}
    for x in range(0, 4):

        #loop through the 4 hemispheres and find the their titles
        hemtitle = souptitle.find_all('div', class_='description')[x].find('h3').text
        #split the title and store the first word
        hem = hemtitle.split(' ', 1)[0]

        #use splinter to visit the website and click on the current hemispheres based on partial text
        browser.visit(marshemi)
        browser.click_link_by_partial_text(hem)

        html = browser.html
        soupimage = BeautifulSoup(html, 'html.parser')

        #find the URL 
        hemimage = soupimage.find('a', target='_blank')['href']

        #add the title & url to the dictionary
        hemisphere_image_urls['title_' + hem] = hemtitle
        hemisphere_image_urls['image_url_' + hem] = hemimage
    
    #create a new dictionary based on all the values previously found
    marsscrape = {
    'news_title' : titleresults,
    'news_desc' : descresults,
    'image': image,
    'tweet': marstweet,
    'table': marstable_html,
    'hemi': hemisphere_image_urls
    }  

    #return the dictionary
    return marsscrape








