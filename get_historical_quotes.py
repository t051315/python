#!/usr/bin/python3
#
# Script Name: get_historical_quotes.py
# Location: ~/Development/python/mymoney
# Description: A Python server script to return security names owned. This
#
# Developer: Louis Lao
# Date: May 9, 2017
#
# Modified By: Louis Lao
# Date: Oct 26, 2017
# Reason: The MongoDB access authorization class is now in a separate
#         module (auth_mongodb.py). Add import statement.
#
# Modified By: Louis Lao
# Date: Dec 31, 2017
# Reason: Output data in a more readable format.


# Import custom module.
import auth_mongodb
import moneyMod1    # Custom module for "mymoney" web app.

# This parameter is the 'query' to the MongoDB collection find() method.
secID = 8

# Global variables for MongoDB access.
__db_auth__  = "mymoney"
__login__    = "money_user"
__password__ = "LLadmin8"
__host__     = "localhost"
__port__     = "27017"

hostDB = auth_mongodb.MongoDB_Login (__host__, __port__,
                   __login__, __password__, __db_auth__)
userDB = hostDB.connect_via_host ()
qry = moneyMod1.Queries_Money (userDB)

pipeline = [
  { "$match"  : {"security_id":secID} },
  { "$unwind" : "$quotes" },
  { "$sort"   : {"quotes.date":-1} },
  { "$group"  : { "_id": "$_id",
                  "security_id"   : {"$max" : "$security_id"},
                  "security_name" : {"$max" : "$security_name"},
                  "owners"        : {"$max" : "$owners"},
                  "quotes"        : {"$push" :
                     {"quote" : "$quotes.close",
                      "date"  : {"$dateToString" : 
                                {'format':"%Y-%m-%d", 'date':"$quotes.date" } },
                      "ytd"   : "$quotes.YTD_Chg"
                     }
                  }
                }
  }
]

cursor = qry.get_security_quotes_by_aggregate (pipeline)

for item in cursor :
  print ("Name: ", item["security_name"], "( ID: ", item["security_id"], ")")  

  for quote in item["quotes"] :
    print ("%s Close: %.2f  (Change) %s" %\
           (quote["date"], quote["quote"], quote["ytd"]))
    
