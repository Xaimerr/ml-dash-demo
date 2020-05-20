import MySQLdb
import pandas as pd
from info import user, psswd, db_name

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user=user,         # your username
                     passwd=psswd, # your password
                     db=db_name)        # the database


#%%
import time, datetime
from random import randint
# prepare a cursor object using cursor() method


cursor = db.cursor()
while True:
    try:
       ts = time.time()
       timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
       cursor.execute("""INSERT into rala (timestampt,state,rssi,evm) values(%s,%s,%s,%s)""",
                      (timestamp,randint(0,4),-0.01*randint(2000,5000),-0.01*randint(2000,5000)))
       db.commit()
       time.sleep(1)
    except:
       db.rollback()
       print("something went wrong")

#%%
# To perform a query, you first need a cursor, and then you can execute queries on it:
# prepare a cursor object using cursor() method

query = "SELECT * FROM rala;"
try:
    # get the query saved on a pandas DF
    df = pd.read_sql_query(query, db)
    print(df)
except:
   print("Error: unable to fetch data")

#%%
db.close()

#%%

