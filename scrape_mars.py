# Import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

# Define function to scrape the data
def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # define URL
    url = "https://redplanetscience.com/"

    # visit the URL via browser
    browser.visit(url)

    # Define the HTML to scrape with bs4
    html = browser.html

    #Create BeautifulSoup object and parse with html parser
    soup = bs(html, 'html.parser')

    #--------------------------
    #------ NEWS ARTICLE ------
    #--------------------------

    # Collect the latest news title and paragraph text
    news_title = soup.find_all('div', class_="content_title")[0].text
    news_paragraph = soup.find_all('div',class_='article_teaser_body')[0].text

    #--------------------------
    #------- MARS IMAGE -------
    #--------------------------

    # Mars featured image to be scraped
    mars_image_url = 'https://spaceimages-mars.com/'
    browser.visit(mars_image_url)
    mars_image_html = browser.html
    image_soup = bs(mars_image_html, 'html.parser')

    # Find the image URL by finding the element it's in. In this case, it's the 'header' class div element
    element = image_soup.find_all('div',class_='header')

    # From printing the header above we can see the featured image URL can be found in the <img class="headerimage fade-in">
    # element within the 'src' sub-element.
    image_string = element[0].find('img', class_='headerimage')['src']
    
    # Combine the image_url and featured_image_url to create the full URL
    featured_image_url = f'{mars_image_url}{image_string}'

    #--------------------------
    #------- MARS FACTS -------
    #--------------------------

    # Mars facts to be scraped
    facts_url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(facts_url)
    
    # Grab the second table in the list as that has the information
    mars_facts_df = tables[1]
    mars_facts_df.columns=['Measurement','Value']
    
    # Convert the pandas data to html string
    mars_html = mars_facts_df.to_html(index=False, justify='center')
    
    # Remove all line breaks
    mars_html.replace('\n','')

    #--------------------------
    #---- MARS HEMISPHERES ----
    #--------------------------
    
    # Mars hemisphere images to be scraped
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemisphere_soup = bs(hemispheres_html, 'html.parser')

    # Create an empty list to store the dictionaries depicting img_url and title
    hemisphere_list_dicts = []

    # Location of the image urls and hemisphere titles for each hemisphere is located in the "collapsible results" class
    hemisphere_results = hemisphere_soup.find('div', class_="collapsible results")

    # Each hemisphere is located in a <div class="item"> element so extract all of them
    each_hemisphere = hemisphere_results.find_all('div', class_="item")

    # Create a loop to grab the img_url and title from each item in the each_hemisphere list
    for hemisphere in each_hemisphere:
        #Collect the title which is found in <h3> element within the original <div class='item'> that we defined
        title = hemisphere.find('h3').text
        
        # Collect img_url by clicking into each hemisphere link
        hemisphere_link = hemisphere.find('a', class_="itemLink product-item")['href']
        
        # Now visit this URL to be able to get the image link
        browser.visit(f'{hemispheres_url}{hemisphere_link}')
        
        # Once the browser visits the site, need to parse this new html
        image_html = browser.html
        hemisphere_img_soup = bs(image_html, 'html.parser')
        
        # The image jpg link is located in the <div class="downloads"> element
        image = hemisphere_img_soup.find('div', class_='downloads')
    #     print(image)
    #     print('--------------------------------')
        
        # The actual URL is located in the first list item
        img_url = image.find('li').a['href']
        
        #Combine the image URL with the base URL
        img_url_full = f'{hemispheres_url}{img_url}'
        
        # Now that we have grabbed the title and the img_url, put them into a dictionary
        hemisphere_dict = {"title":title,
                        "img_url":img_url_full}
        
        # Append this dictionary to the original list created
        hemisphere_list_dicts.append(hemisphere_dict)

    # Store all the data into a dictionary to return
    mars_dict = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_html),
        "hemisphere_images": hemisphere_list_dicts
    }

    return mars_dict