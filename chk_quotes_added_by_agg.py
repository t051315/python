#!/usr/bin/python3
#
# Script Name: chk_quotes_added_by_agg.py
# Location: ~/Development/python/mymoney
# Description: After adding month-end quotes to all the active securities,
#              running this script will provide a more compact, easy way 
#              to see if all the quotes have been added properly. Finding
#              this using MongoDB shell or other techniques has proven to
#              be very awkward.
#
# Developer: Louis Lao
# Date: Dec 30, 2017
#
# Modified By:
# Date:
# Reason:

# Import custom module.
import sys
import auth_mongodb
import moneyMod1    # Custom module for "mymoney" web app.
import re

import datetime
from bson.json_util import dumps, loads

# This parameter is the 'query' to the MongoDB collection find() method.
mydate = datetime.datetime.strptime ("2017-12-29", "%Y-%m-%d")

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

# Define a pipeline to get the data.
pipeline = [
  { "$unwind"  : "$quotes" },
  { "$match"   : {"quotes.date":mydate} },
  { "$project" : { "_id": 0, "security_name":1, "quotes": 1,
                   "insensitive": {"$toLower": "$security_name"} }},
  { "$sort"    : {"insensitive": 1} }
]

# Get the desired data document and store it in a dict.
cursor = qry.get_security_quotes_by_aggregate (pipeline)

counter = 0
for item in cursor :
  counter = counter + 1
  print (str(counter) + ")", item["security_name"])
  print ("  ", item["quotes"]["close"], "(", item["quotes"]["YTD_Chg"], ")")

