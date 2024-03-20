# This script pulls web page from prior.by, executes java script on it using selenium and stores result in postgres staging table.
# This raw data will be furter processed by another script to extract data on currency rates.
# leotepl@gmail.com 

import urllib.request
import psycopg2
import argparse
import datetime
 
# using now() to get current time
current_time = datetime.datetime.now() 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

parser= argparse.ArgumentParser(description='Pull front page from prior.by')
parser.add_argument('env',metavar='1',type=str,nargs='?',help='environment, prod or dev')
args=parser.parse_args()

# Function to place raw page html content into staging table raw.prior_web_content

def insert_content(content):
    """ Insert into the table """

    sql = """INSERT INTO raw.prior_web_content(content,insert_timestamp)
             VALUES(%s,current_timestamp) RETURNING record_id;"""                    # SQL to insert the row
    
    record_id = None        # the record_id will be assigned by Postgres sequence as default value
#    config = load_config()

    try:
                # password is not present in the statement, it is taken from ~/.pgpass file by
        with  psycopg2.connect(dbname="currency_rates_"+args.env, user="postgres", host="127.0.0.1", port="5432") as conn: 
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (content,))

                # get the generated id back                
                rows = cur.fetchone()
                if rows:
                    record_id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(parser.prog+datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")+" : exception :",error)    
    finally:
        return record_id   # function returns generated record_id
    

print(parser.prog+": "+datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")+" started on "+args.env )

# initialize selenium

op = webdriver.ChromeOptions()
op.add_argument('--headless')
driver = webdriver.Chrome(options=op,service=ChromeService(ChromeDriverManager().install()))

driver.get("https://www.prior.by/web/")                                 # get source page
innerHTML = driver.execute_script("return document.body.innerHTML")     # execute script on source


r=insert_content(innerHTML)    # inssert html content to staging table

print(parser.prog+":"+" Record #",r,"added to staging.")