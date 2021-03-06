# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
 
# Path to chromedriver
# !which chromedriver

# # Set the executable path and initialize the chrome browser in splinter
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path)

def mars_news(browser):
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
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        
        slide_elem.find("div", class_='content_title')
        
        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p
 
# ## JPL Space Images Featured Image
def featured_image(browser): 
    # Visit URL

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    print(f'Opening URL:{url}')
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None
        
    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url
    
# ## Mars Facts
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
    return df.to_html(classes="table table-striped")

def get_hemispheres(browser):
    # browser = Browser("chrome", executable_path="chromedriver", headless=True)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("div.collapsible.results", wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    info= []
    try:
        all_hems = news_soup.find_all('div', class_='item')
        for hem in all_hems:
            d = {}
            d["title"] = hem.h3.text
            d["img_url"] = f"https://astrogeology.usgs.gov{hem.img['src']}"
            d["full_url"] = f"https://astrogeology.usgs.gov{hem.a['href']}"
            d["description"] = hem.p.text
            info.append(d)    
    except AttributeError:
        return None

    #return pd.DataFrame(info)
    return info

    
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": get_hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
    