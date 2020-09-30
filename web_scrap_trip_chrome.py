from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

driver = None

try:
    DRIVER_PATH = 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    ## VISITING THE WEBSITE
    driver.get('https://www.tripadvisor.com/')

    ## CLICKING THE HOTEL ICON
    hotel_button = driver.find_element_by_xpath('/html/body/div[1]/main/div[1]/div[1]/div/div/div[1]/a')
    hotel_button.click()

    ## SEARCHING FOR HOTELS IN NEW DELHI
    city = 'New Delhi'
    search_bar = driver.find_elements_by_name("q")[2]
    search_bar.send_keys(city)
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[3]/div/form/div/a[1]').click()

    current_url = driver.current_url
    print(current_url)
    time.sleep(10)

    # GETTING NAMES AND LINKS OF THE IMAGES OF THE HOTELS 
    html_list = driver.find_elements_by_class_name("listing_title")
    Hotel_names = []
    Img_links = []
    for i,item in enumerate(html_list):
        print("Name:" + str(i+1))
        # it = item.find_elements_by_name(By.tagName("a"))
        text = str(item.text)
        Hotel_names.append(text)
        print(text)
        img_link = item.find_element_by_tag_name('a')
        Img_links.append(img_link.get_attribute("href"))

    # GETTING THE PRICES
    html_list = driver.find_elements_by_class_name("price-wrap ") 
    Prices = []
    for i,item in enumerate(html_list):
        html_price = item.find_element_by_class_name("price.__resizeWatch") 
        print("Price:" + str(i+1))
        text = str(html_price.text)
        Prices.append(text)
        print(text)

    # GETTING THE AMENITIES
    html_list = driver.find_elements_by_class_name("info-col")
    Amenities = []
    for item in html_list:
        html_amenities = item.find_elements_by_class_name("text")
        temp = []
        for subitem in html_amenities:
            text = str(subitem.text)
            if (text != "Taking safety measures") and (text != "Visit hotel website") and (text != "Special offer"):
                temp.append(text)
        Amenities.append(temp)
    print(Amenities)

    time.sleep(5)

    # CREATING THE CSV FILE
    df = pd.DataFrame(columns = ['Hotel Names','Price','Amenities','Images'])
    df['Hotel Names'] = Hotel_names
    df['Price'] = Prices
    df['Amenities'] = Amenities
    df['Images'] = Img_links 
    df.to_csv('Hotel_data.csv', index = False) 

except:
    #pass
    print("Exception occurred!")
    if driver is not None:
        driver.__exit__()
