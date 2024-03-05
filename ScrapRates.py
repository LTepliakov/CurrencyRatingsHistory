from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

#from bs4 import BeautifulSoup

#import re

import pandas as pd
pd.options.display.width = 0

from ScrapCurrRatesPrior import scrapCurrRatesPrior 

op = webdriver.ChromeOptions()
op.add_argument('--headless')
driver = webdriver.Chrome(options=op,service=ChromeService(ChromeDriverManager().install()))


#driver = webdriver.Chrome(options=op)
#driver.get("https://www.prior.by/web/")
#innerHTML = driver.execute_script("return document.body.innerHTML")


file = open("inner.html", "r")
page = file.read()
file.close()
        

df=scrapCurrRatesPrior(page)

print(df)
                

df.to_pickle("CurrencyRates.pkl") 