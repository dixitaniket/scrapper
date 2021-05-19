from datetime import datetime


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
chrome_options=Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options,executable_path="/home/aniket/Documents/aggregatrocdoe/PancakeSwap-Price-Scraper/scraper/chromedriver")
farms_endpoint="https://pancakeswap.finance/farms"

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time



# SCROLL_PAUSE_TIME = 1

# last_height = driver.execute_script("return document.body.scrollHeight")
# # driver.get(farms_endpoint)
# sleep(15)

# for scrapping data of the farms having pairs
def scrape_farms(driver):

    SCROLL_PAUSE_TIME = 1

    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.get(farms_endpoint)
    sleep(15)
    def return_xpaths_farms(td):
        mapper={}
        mapper["apr"]=f'//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[{td}]/td[3]/div/div/div[2]/div/div'
        mapper["pairname"]=f'//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[{td}]/td[1]/div/div/div/div/div[2]/div'
        mapper["liquidity"]=f'//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[{td}]/td[4]/div/div/div[2]/div/div[1]/div'
        # mapper["multiplier"]=f'//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/table/tbody/tr[1]/td[{td}]/div/div/div[2]/div/div[1]'
        return mapper
    
    for i in range(12):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # data handling section
    pandasmapper={}
    listover=False
    import pandas as pd
    for i in range(1,300):
        data=return_xpaths_farms(i)
        for detail,xpath in data.items():
            try:
                text=WebDriverWait(driver,timeout=20).until(lambda d : d.find_element_by_xpath(xpath))
            except:
                listover=True
                break
                
            if detail not in pandasmapper.keys():
                pandasmapper[detail]=[text.text]
            else:
                pandasmapper[detail].append(text.text)
            if text.text=="" or text.text==None:
                print("not loaded properly")
            print(f"{detail}> ",text.text)
        if listover:
            break
    dataframe=pd.DataFrame(pandasmapper)
    dataframe.to_csv("farms_scrapped.csv")
# dataframe.to
scrape_farms(driver)

def scrape_pools(driver):
    SCROLL_PAUSE_TIME = 1

    last_height = driver.execute_script("return document.body.scrollHeight")
    pools_endpoint="https://pancakeswap.finance/pools"
    driver.get(pools_endpoint)
    sleep(15)

    def return_xpaths_pools(i):
        mapper={}
        mapper["Pool_Name"]=f'//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div[{i}]/div/div[1]/div/div[1]/h2'
        mapper["Stake_Name"]=f'//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div[{i}]/div/div[1]/div/div[1]/div'
        mapper["pool_apr"]=f'//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div[{i}]/div/div[2]/div[1]/div[2]/div/span[1]'
        button_xpath=f'//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div[{i}]/div/div[3]/div/button'
        mapper["total_Cake_Staked"]=f'//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div[{i}]/div/div[3]/div[2]/div[1]/div[2]/div[1]/span'
        return mapper,button_xpath

    for i in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    pandasmapper={}
    sleep(10)
    listover=False
    import pandas as pd
    for i in range(2,20):
        data,button_xpath=return_xpaths_pools(i)
        driver.find_element_by_xpath(button_xpath).click()
        for detail,xpath in data.items():
            try:
                text=WebDriverWait(driver,timeout=20).until(lambda d : d.find_element_by_xpath(xpath))
            except:
                listover=True
                break
                
            if detail not in pandasmapper.keys():
                pandasmapper[detail]=[text.text]
            else:
                pandasmapper[detail].append(text.text)
            if text.text=="" or text.text==None:
                print("not loaded properly")
            print(f"{detail}> ",text.text)
        if listover:
            break
    dataframe=pd.DataFrame(pandasmapper)
    dataframe.to_csv("pools_scrapped.csv")
#scrape_pools(driver)




