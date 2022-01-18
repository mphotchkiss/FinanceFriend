import sqlite3

#connect to the DB
conn = sqlite3.connect("transaction_cache2.db")
c = conn.cursor()

c.execute("SELECT month, oid FROM transactions")
trans = c.fetchall()

for tran in trans:
    month = tran[0]
    print(month)
#    if(int(month)<10):
#        new = month.strip("0")
#        new = "0" + new
#        c.execute("UPDATE transactions SET month=(:new) WHERE oid=(:oid)", {
#            'new': new,
#            'oid':tran[1]
#        })

#close connection
conn.commit()
conn.close()