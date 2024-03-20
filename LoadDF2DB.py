# LoadDF2DB
# 
# This module provides loadDF2DB function which loads currency rates data into database 
# It takes three input parameters:
# - dataframe with currency rates intofmation
# - timestamp of a raw record (file), from which this information was scrapped
# - environment (dev or prod) to which dataframe data will be loaded.
#
# leotepl@gmail.com 

import psycopg2
import pandas as pd



def loadDF2DB(df,timestamp,env):
    
    #   prepare keys dataframe from which  primary key values will be loaded into prior.currency_rate_history table
    keys=df[['client_currency_code','bank_currency_code','operation_place','operation_code','valid_from_datetime']].drop_duplicates().reset_index()

    #  The query to insert data to prior.currency_rate_history. The row is inserted only if the row with same key values does not already exists.
    #  It may happen that the raw page was pulled from the site by the schedule, but bank did not change rates since previous pull.
    #  The query returns ID of inserted record to use as a reference in the child table
    sql1="""
    INSERT INTO prior.currency_rate_history
            (  client_currency_code,     bank_currency_code,     operation_place_code,     operation_code,     valid_from_datetime,     raw_data_timestamp)
    SELECT   %(client_currency_code)s, %(bank_currency_code)s, %(operation_place)s,      %(operation_code)s, %(valid_from_datetime)s, %(raw_data_timestamp)s

    WHERE
    NOT EXISTS (
    SELECT * FROM prior.currency_rate_history 
    WHERE client_currency_code = %(client_currency_code)s
    AND bank_currency_code   = %(bank_currency_code)s
    AND operation_place_code = %(operation_place)s
    AND operation_code       = %(operation_code)s
    AND valid_from_datetime  = %(valid_from_datetime)s
    )
    RETURNING currency_rate_list_id ;

    """


    # The query to insert currency rates to child table.
    sql2="""
    INSERT INTO prior.currency_rate_list
            (currency_rate_list_id,     currency_buy_rate,     buy_rate_coefficient,     currency_sell_rate,     sell_rate_coefficient,     low_limit_amount,     high_limit_amount)
    VALUES( %(currency_rate_list_id)s, %(currency_buy_rate)s, %(buy_rate_coefficient)s, %(currency_sell_rate)s, %(sell_rate_coefficient)s, %(low_limit_amount)s, %(high_limit_amount)s)
    ;
    """

    # CHeck that current keys of data to be inserted are not already in the table. 
    sql3="""
    select count(*) from prior.currency_rate_history
    where client_currency_code  = %(client_currency_code)s
    AND bank_currency_code   = %(bank_currency_code)s
    AND operation_place_code = %(operation_place)s
    AND operation_code       = %(operation_code)s
    AND valid_from_datetime  = %(valid_from_datetime)s
    ;
    """

    try:
        with  psycopg2.connect(dbname="currency_rates_"+env\
                            , user="postgres"\
                            , host="127.0.0.1"\
                            , port="5432") as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statements
                for ind in keys.index:
                    cur.execute(sql3,
                                {'client_currency_code':keys['client_currency_code'][ind],
                                'bank_currency_code':keys['bank_currency_code'][ind],
                                'operation_place':keys['operation_place'][ind],
                                'operation_code':keys['operation_code'][ind],
                                'valid_from_datetime':keys['valid_from_datetime'][ind]
                                })
                    count=cur.fetchone()[0]
                    if count==0:                # go ahead with insertion only if this key is not already in the parent table.                
                        cur.execute(sql1,
                                {'client_currency_code':keys['client_currency_code'][ind],
                                'bank_currency_code':keys['bank_currency_code'][ind],
                                'operation_place':keys['operation_place'][ind],
                                'operation_code':keys['operation_code'][ind],
                                'valid_from_datetime':keys['valid_from_datetime'][ind],
                                'raw_data_timestamp':timestamp
                                })
                    
                        currency_list_id=cur.fetchone()[0]   # ID of parent table record to be used as a reference in the child
 
                        #  get the currency rates data rows to be inserted to child table
                        currency_list=df[(keys['client_currency_code'][ind]==df['client_currency_code']) &
                                        (keys['bank_currency_code'][ind]==df['bank_currency_code']) &
                                        (keys['operation_place'][ind]==df['operation_place']) &
                                        (keys['operation_code'][ind]==df['operation_code']) &
                                        (keys['valid_from_datetime'][ind]==df['valid_from_datetime']) 
                                        ]
                        # insert into child table
                        for l in currency_list.index:
                            cur.execute(sql2,
                                        {'currency_rate_list_id':currency_list_id,      # ref to parent table
                                        'currency_buy_rate':currency_list['currency_buy_rate'][l],   
                                        'buy_rate_coefficient':currency_list['buy_rate_coefficient'][l],
                                        'currency_sell_rate':currency_list['currency_sell_rate'][l],
                                        'sell_rate_coefficient':currency_list['sell_rate_coefficient'][l],
                                        'low_limit_amount':currency_list['low_limit'][l],
                                        'high_limit_amount':currency_list['high_limit'][l]
                                        }
                                    )
                
                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print('LoadDF2DB: exception: ',error)    

