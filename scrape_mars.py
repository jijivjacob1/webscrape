# Dependencies
import time
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd



def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Retrieve page with the requests module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title =  soup.find("div", class_="content_title").text
    # print(news_title )

    news_p = soup.find("div", class_="article_teaser_body").text
    # print(news_p)

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html

    browser.click_link_by_partial_text("FULL")
    time.sleep(1)

    browser.click_link_by_partial_text("more info")
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_sec = soup.find("aside", class_="image_detail_module")

    result_ptags = image_sec.find_all("p")

    # Loop through returned results
    for result in result_ptags:
        if (result.text.startswith("Full-Res JPG") ):
            jpg_url = result.find("a")["href"]

    browser.click_link_by_partial_href(jpg_url)
    time.sleep(1)

    featured_image_url = browser.url
    # print(featured_image_url)

    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    time.sleep(1)
    weather_soup = BeautifulSoup(response.text, 'html.parser')

    result_tweets = weather_soup.find_all('p',class_="tweet-text")
    # print(result_tweets)

    # Loop through returned results
    for result in result_tweets:
        if (result.text.startswith("Sol ") ):
            mars_weather = result.text
            break

    # print(mars_weather)

    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df_facts = tables[0]
    df_facts.columns = ["Facts","Value"]
    df_facts.set_index("Facts",inplace =True)
    fact_html_table = df_facts.to_html()
    fact_html_table = fact_html_table.replace("\n","")

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hem_link = soup.find_all("a",class_="itemLink")

    hemisphere_image_urls = []
    for hem in hem_link:
        hem_dict={}
        if hem.find('h3'):
            hem_dict["title"] = hem.h3.text
            #         print( hem["href"])
            #         print( hem.h3.text)
            time.sleep(2)
            #browser.click_link_by_partial_href(hem["href"])
            browser.click_link_by_partial_text(hem.h3.text)
            time.sleep(2)
            html = browser.html
            soup_inner = BeautifulSoup(html, 'html.parser')
            download_div = soup_inner.find('div',class_="downloads")
            #         print(download_div.find("a")["href"])
            hem_dict["img_url"] = download_div.find("a")["href"]
            browser.click_link_by_text("Back")
            time.sleep(2)
            hemisphere_image_urls.append(hem_dict)

    # print(hemisphere_image_urls)

    scrape_data = {
        "news_title" : news_title,
        "news_p" : news_p,
        "featured_image_url" : featured_image_url,
        "mars_weather" : mars_weather,
        "fact_html_table" : fact_html_table,
        "hemisphere_image_urls" : hemisphere_image_urls
    }

    print(scrape_data)


    return scrape_data


# scrape()