from selenium import webdriver
from selenium.webdriver.common.by import By
from db import db


# Get the number of total pages
def calculate_pages(PATH, product_type):
    """
        function calculates the total number of pages to be scraped
        params:
            PATH (str): path of chrome driver
            product_type (str): type of product
        return:
            total_pages (int): total number of pages
    """

    driver = webdriver.Chrome(PATH)
    driver.get(f'https://www.flipkart.com/search?q={product_type}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off')

    # For grid view
    pages = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[12]/div/div/span[1]')

    # For list view
    # pages = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[26]/div/div/span[1]')
    

    total_pages = int(pages.text.split(" ")[-1].replace(',', ''))
    print("total_pages", total_pages)
    return total_pages


# Create connection with webdriver
def create_conn(PATH, product_type, page):
    """
        creates connection of webdriver with the url
        params:
            PATH (str): path of chrome driver
            product_type (str): type of product
        return:
            driver (webdriver instance): the webdriver instance
    """

    driver = webdriver.Chrome(PATH)
    driver.get(f'https://www.flipkart.com/search?q={product_type}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page}')

    return driver


# Scrape data from the webpage having grid view data
def get_data(driver, category, product_type):
    """
        function scrapes the data (grid view) of speciified url and stores the data in db
        params:
            driver (webdriver instance): the webdriver instance
            category (str): category of product
            product_type (str): type of product
    """

    containers = driver.find_element(By.CSS_SELECTOR, value='#container > div > div._36fx1h._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div:nth-child(2)')
    
    divs = containers.find_elements(By.CLASS_NAME, '_1AtVbE')


    if len(divs) == 0:
        return

    for div in divs:
        product_name = div.find_elements(By.CLASS_NAME, '_2WkVRV')
        product_image = div.find_elements(By.CLASS_NAME, '_2r_T1I')
        product_detail = div.find_elements(By.CLASS_NAME, 'IRpwTa')
        product_price = div.find_elements(By.CLASS_NAME, '_30jeq3')
        data_list = []
        for i in range(0, len(product_name)):
            data_list.append({
                'name': product_name[i].text,
                'image': product_image[i].get_attribute('src'),
                'detail': product_detail[i].text,
                'price': product_price[i].text,
                'product_type': product_type
            })
        
        try:
            print(data_list)
            db[category].insert_many(data_list)
        except TypeError:
                pass


# Scrape data from the webpage having list view data
def get_list_view_data(driver, category, product_type):
    """
        function scrapes the data (list view) of speciified url and stores the data in db
        params:
            driver (webdriver instance): the webdriver instance
            category (str): category of product
            product_type (str): type of product
    """

    containers = driver.find_element(By.CSS_SELECTOR, value='#container > div > div._36fx1h._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div:nth-child(2)')
    
    divs = containers.find_elements(By.CLASS_NAME, '_1AtVbE')
    

    if len(divs) == 0:
        return

    for div in divs:
        detail_list = []
        uls = div.find_elements(By.CSS_SELECTOR, '.fMghEO')
        for ul in uls:

            lis = ul.find_elements(By.CLASS_NAME, 'rgWa7D')

            for li in lis:
                detail_list.append(li.text)

        product_name = div.find_elements(By.CLASS_NAME, '_4rR01T')
        product_image = div.find_elements(By.CLASS_NAME, '_396cs4')
        product_price = div.find_elements(By.CLASS_NAME, '_30jeq3')
        product_details = detail_list

        data_list = []

        for i in range(0, len(product_name)):
            data_list.append({
                'name': product_name[i].text,
                'image': product_image[i].get_attribute('src'),
                'detail': product_details,
                'price': product_price[i].text,
                'product_type': product_type
            })

        try:
            db[category].insert_many(data_list)
        except TypeError:
                pass
      

# Quit the connection to webdriver
def quit_conn(driver):
    """
        function quits the webdriver instance
        params:
            driver (webdriver instance): the webdriver instance
    """

    driver.quit()