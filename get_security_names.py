#!/usr/bin/python3
#
# Script Name: get_security_names.py
# Location   : /home/louis/Development/python/mymoney
# Description: A Python server script to return security names owned. This
#              script accepts a parameter indicating what type of names
#              the calling script wants. This parameter is the status of
#              the security which can be either 'active' or 'inactive'.
#              It will also accept the parameter value of 'all' which will
#              instruct the script to return all names in the database.
#
# Developer: Louis Lao
# Date: Nov 1, 2016
#
# Modified By: Louis Lao
# Date: Nov 8, 2016
# Reasons: 1) Instead of coding this cgi script to retrieve securitiy names
#             based on the value of 'status', I made it more general by
#             accepting a query object instead so that this can return names
#             of security based on the MongoDB collection's 'find' method's
#             'query' parameter. This also means that as long as you can 
#             pass to it the 'query' parameter, this script will return
#             a list of security names in a string format.
#          2) Because of the need to transfer the 'query' parameter from
#             javascript to Python, it is necessary to make the javascript
#             object a string and then convert it back to a Python object
#             here, I need to import the 'loads' moduke from json_util.
#
# Modified By: Louis Lao
# Date: Oct 26, 2017
# Reason: The MongoDB access authorization class is now in a separate
#         module (auth_mongodb.py). Add import statement.

#
# How to execute this script: 
#   python get_security_names.py {\"status\":\"inactive\"}
#

# Import custom modules.
import sys
import auth_mongodb
import moneyMod1    # Custom module for "mymoney" web app.
import re

from bson.json_util import dumps, loads

# This parameter is the 'query' to the MongoDB collection find() method.
#what = loads(params["what"].value)
what = {"owners":"Louis"}

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

# Get the desired data document and store it in a dict.
doc = {}
json_out = ""
cursor = qry.get_security_names (what)

for item in cursor :
  doc["security_id"] = item["security_id"]
  doc["security_name"] = item["security_name"]
  doc["status"] = item["status"]

  # Serialize the object to a JSON formatted string format.
  #json_out += dumps(doc)
  json_out += dumps(doc) + "::"

  # Reset the dictionary for the next security.
  doc = {}

# Remove the last string token '::'.
json_out = re.sub(r"::$", "", json_out)
json_out = json_out.split("::")

counter = 0
for item in json_out:
  counter += 1
  print (counter, ')', item)

