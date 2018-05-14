from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests


def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
 
    mars_news_url = "https://mars.nasa.gov/news/"
    response = requests.get(mars_news_url)
    soup = bs(response.text, 'html.parser')
    news_title = soup.find('div', class_='content_title').text.strip()
    news_p = soup.find('div', class_='image_and_description_container').text.strip()
     
    mars_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    alist = soup.find_all('a', class_='button fancybox')
    for a in alist:
        link = a['data-fancybox-href']
        featured_image_url = 'https://www.jpl.nasa.gov/' + link
        print(featured_image_url)

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)    
    html = browser.html
    soup = bs(html, 'html.parser')

    weathers = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    weather = weathers[0].text

    print(weather)
    
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)

    df = tables[0]
    df.head()
    
    html_table = df.to_html()
    df.to_html('table.html')
    html_table
    
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemis_url)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    items = soup.find_all('div', class_ = 'item')

    hemisphere_image_urls = [];

    for item in items:
        description = item.find('div', class_ = 'description')
        hemisphere = description.find('a', class_= 'itemLink product-item')
        title = hemisphere.find('h3').text

        img_a = item.find('a', class_= 'itemLink product-item')
        img_url = 'https://astrogeology.usgs.gov' + img_a['href']

        hemi_dict = {}
        hemi_dict['title'] = title
        hemi_dict['img_url'] = img_url

        hemisphere_image_urls.append(hemi_dict)
    
    
    
    print(hemisphere_image_urls)

    return {"title": news_title, 
            "paragraph": news_p,
            "image_url": featured_image_url,
            "weather": weather,
            "facts": html_table,
            "hemisphere_image": hemisphere_image_urls
           }