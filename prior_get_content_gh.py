import datetime

 
# using now() to get current time
current_time = datetime.datetime.now()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

file_name='prior_page_'+datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")+'.html'
print('file name:',file_name)

op = webdriver.ChromeOptions()
op.add_argument('--headless')
driver = webdriver.Chrome(options=op,service=ChromeService(ChromeDriverManager().install()))

driver.get("https://www.prior.by/web/")
innerHTML = driver.execute_script("return document.body.innerHTML")

with open(file_name,'w') as out_file:
    out_file.write(innerHTML)

