#!/usr/bin/env python
# coding: utf-8

# In[57]:

def scrape():


    from bs4 import BeautifulSoup
    import requests
    import pymongo
    from splinter import Browser
    import pandas as pd


    # In[10]:


    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'


    # In[11]:


    # Retrieve page with the requests module
    response = requests.get(url)


    # In[12]:


    soup = BeautifulSoup(response.text, 'html.parser')


    # In[24]:


    titleresults = soup.find('div', class_='content_title').a.text.strip()
    descresults = soup.find('div', class_='rollover_description_inner').text.strip()
    

    # In[40]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)


    # In[41]:


    splinterlink = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(splinterlink)


    # In[42]:


    browser.click_link_by_id('full_image')


    # In[49]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = "https://www.jpl.nasa.gov" + soup.find('a', class_='button fancybox')['data-fancybox-href']


    # In[55]:


    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    # In[56]:


    marstweet = soup.find_all('div', class_='js-tweet-text-container')[0].text.strip()
    marstweet


    # In[81]:


    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    marstable_df = tables[0]
    marstable_df.columns = ['Stats', 'Values']
    marstable_df.set_index('Stats', inplace=True)
    marstable_df.head()


    # In[84]:


    marstable_html = marstable_df.to_html()
    marstable_html = marstable_html.replace('\n', '')
    #or marstable_df.to_html(marstable.html)


    # In[104]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    marshemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(marshemi)
    souptitle = BeautifulSoup(response.text, 'html.parser')


    # In[105]:


    hem = []
    hemisphere_image_urls = []
    for x in range(0, 4):

        hemtitle = souptitle.find_all('div', class_='description')[x].find('h3').text
        hem = hemtitle.split(' ', 1)[0]

        browser.visit(marshemi)
        browser.click_link_by_partial_text(hem)

        html = browser.html
        soupimage = BeautifulSoup(html, 'html.parser')

        hemimage = soupimage.find('a', target='_blank')['href']

        marsdic = {
            'title': hemtitle,
            'image_url': hemimage
        }
        hemisphere_image_urls.append(marsdic)

    hemisphere_image_urls
    
    marsscrape = {
    '1' : titleresults
    '2' : descresults
    '3': image,
    '4': marstweet,
    '5': marstable_html,
    '6': hemisphere_image_urls
    }





