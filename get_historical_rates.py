#!/usr/bin/python3
#
# Script Name: get_historical_rates.py
# Location: ~/Development/python/mymoney
# Description: A Python server script to return all rates and indexes data.
#
# Developer: Louis Lao
# Date: May 15, 2017
#
# Modified By: Louis Lao
# Date: Oct 26, 2017
# Reason: The MongoDB access authorization class is now in a separate
#         module (auth_mongodb.py). Add import statement.
#
# Modified By: Louis Lao
# Date: Dec 31, 2017
# Reason: Expand the report to include the possibility of Bitcoin values.

# Import custom modules.
import auth_mongodb
import moneyMod1    # Custom module for "mymoney" web app.


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

# Get the desired data and store it in an array of objects.
cursor = qry.get_all_rates ( )

for item in cursor :
  mydate = item["date"].strftime ('%Y-%m-%d') 
  print ("%s  (Dow) %.2f  (TSX) %.2f  (Exchange) %.4f" %\
         (mydate, float(item['dow']), float(item['tsx']), item['exchrate']), end=" ")

  if ("bitcoin" in item) :
    print (" (Bitcoin) %.2f" % (float(item["bitcoin"])))
  else :
    print ()

