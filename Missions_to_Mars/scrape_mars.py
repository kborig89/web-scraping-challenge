#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


#get_ipython().system('which chromedriver')


# In[3]:
def scrape_info():

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[4]:


    #URL for NASA Mars news
    nasa_url='https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    html=browser.html

    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html=browser.html
    # In[5]:


    #Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')


    # In[10]:


    #Extract most recent article title and teaser
    latest_news=soup.find("div", class_="list_text")
    news_title=latest_news.find("div", class_="content_title").text
    news_p=latest_news.find("div", class_="article_teaser_body").text

    print(news_title)
    print(news_p)


    # In[ ]:





    # In[15]:


    #URL for featured image
    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    image_button=browser.find_by_id("full_image")
    image_button.click()
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_button=browser.links.find_by_partial_text("more info")
    more_info_button.click()


    # In[16]:


    #Parse with BeautifulSoup
    html=browser.html
    feat_image_soup=BeautifulSoup(html,"html.parser")
    image_scrape_url=feat_image_soup.find("figure", class_="lede").a["href"]
    print(image_scrape_url)
    full_image_url="https://www.jpl.nasa.gov"+image_scrape_url

    # In[17]:


    #mars facts url
    mars_facts_url="https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    html = browser.html


    # In[18]:


    #use pandas to scrape facts
    table = pd.read_html(mars_facts_url)
    mars_table_facts=table[1]
    print(mars_table_facts)


    # In[19]:


    #use pandas to convert data to html table string
    mars_facts=mars_table_facts.to_html()


    # In[22]:


    hem_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)


    # In[23]:


    hem_image_urls=[]
    results=browser.find_by_css("a.product-item h3")
   
   


    # In[24]:


    for i in range(len(results)):
        hemisphere={}
        browser.find_by_css("a.product-item h3")[i].click()
        image_url=browser.links.find_by_text('Sample').first['href']
        title=browser.find_by_css("h2.title").text
        hemisphere["img_url"]=image_url
        hemisphere["title"]=title
        hem_image_urls.append(hemisphere)
        browser.back()
        
  

    # In[25]:


    hem_image_urls



# Store data in a dictionary
    mars_data = {
        "hem_image_urls": hem_image_urls,
        "mars_fact": mars_facts,
        "full_image_url": full_image_url,
        "news_p":news_p,
        "news_title":news_title
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

if __name__ == "__main__":
    print(scrape_info())


