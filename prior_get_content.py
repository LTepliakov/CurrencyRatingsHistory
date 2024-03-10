import urllib.request
import psycopg2
import argparse
import datetime

 
# using now() to get current time
current_time = datetime.datetime.now()
 
# Printing value of now.
print("Time now at greenwich meridian is:", current_time)


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager



parser= argparse.ArgumentParser(description='Pull front page from prior.by')
parser.add_argument('env',metavar='1',type=str,nargs='?',help='environment, prod or dev')
args=parser.parse_args()

def insert_content(content):
    """ Insert into the table """

    sql = """INSERT INTO raw.prior_web_content(content,insert_timestamp)
             VALUES(%s,current_timestamp) RETURNING record_id;"""
    
    record_id = None
#    config = load_config()

    try:
        with  psycopg2.connect(dbname="currency_rates_"+args.env, user="postgres",password="robirp", host="127.0.0.1", port="5432") as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (content,))

                # get the generated id back                
                rows = cur.fetchone()
                if rows:
                    vendor_id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return record_id
    

print(datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")+"  --------------")

#driver = webdriver.Chrome()
#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
op = webdriver.ChromeOptions()
op.add_argument('--headless')
driver = webdriver.Chrome(options=op,service=ChromeService(ChromeDriverManager().install()))

driver.get("https://www.prior.by/web/")
innerHTML = driver.execute_script("return document.body.innerHTML")


#with urllib.request.urlopen('https://www.prior.by/web/') as f:
#    cont=f.read().decode('utf-8')

# print(cont)

insert_content(innerHTML)    

