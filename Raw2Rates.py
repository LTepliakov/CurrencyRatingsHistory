import psycopg2
import argparse

from ScrapCurrRatesPrior import scrapCurrRatesPrior 
from LoadDF2DB import loadDF2DB

parser= argparse.ArgumentParser(description='Pull front page from prior.by')
parser.add_argument('env',metavar='1',type=str,nargs='?',help='environment, prod or dev')
args=parser.parse_args()
#print (args.env,type(args.env))
#exit()


getLastUpdateTS="""
select max(raw_data_timestamp) from prior.currency_rate_history
"""
getNewRawData="""
select 
 record_id
,content
,insert_timestamp
from raw.prior_web_content
where insert_timestamp > %(last_load_timestamp)s --'2024-03-06 14:50:14.324429+03:00'
"""

try:

    with  psycopg2.connect(dbname="currency_rates_"+args.env\
                           , user="postgres"\
                           , host="127.0.0.1"\
                           , port="5432") as conn:
        with  conn.cursor(getLastUpdateTS) as cur:
            cur.execute(getLastUpdateTS)
            row=cur.fetchone()
            print ('---',row[0])
            if row[0] is None:
                ts='2000-01-01 00:00:00.0+03:00'
#                print('a')
            else:
                ts=row[0]
#                print('b')
#            print('---',ts)

    with  psycopg2.connect(dbname="currency_rates_"+args.env\
                           , user="postgres"\
                           , host="127.0.0.1"\
                           , port="5432") as conn:
        with  conn.cursor() as cur:
            # execute the INSERT statement
            cur.execute(getNewRawData,{'last_load_timestamp':ts})
            for row in cur:
                
                content=row[1] #.replace('\r\n','\n')
                timestamp=row[2]
                print(row[2])

                df=scrapCurrRatesPrior(content) 
#                df.to_pickle("./dummy.pkl")                   
                loadDF2DB(df,timestamp,args.env)
except (Exception, psycopg2.DatabaseError) as error:
    print(error)    

