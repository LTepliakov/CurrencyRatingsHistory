# This script pulls page from www.prior.by using selenium, executes java on it and saves result in html file, 
# File name contains timestamp of the moment when it is done.
# The script is run by GitHub action on crontab schedlule. GitHub action commits the file to repository.
# Time to time Raw2RatesGH.py script on PC pulls newly comitted files from GitHub, scraps currency rates data into database and removes them from repository.
#
# 
#
# leotepl@gmail.com

import datetime
 
# using now() to get current time
current_time = datetime.datetime.now()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

file_name='prior_page_'+datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")+'.html'  # file name contains timestamp.

# Initialize selenium driver

op = webdriver.ChromeOptions()
op.add_argument('--headless')
driver = webdriver.Chrome(options=op,service=ChromeService(ChromeDriverManager().install()))

driver.get("https://www.prior.by/web/")                                # pull the page
innerHTML = driver.execute_script("return document.body.innerHTML")    # execute java script on the page

with open(file_name,'w') as out_file:                                  # save the page to file
    out_file.write(innerHTML)

with open("html_file_name.txt",'w') as file_name_file:  #  we place the name of file with saved page into file "html_file_name.txt" 
    file_name_file.write(file_name)                     #  it will be used on the next step by the script that will will scrap html and load currrency  
                                                        #  rates data into the database on the cloud
