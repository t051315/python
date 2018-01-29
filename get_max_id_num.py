#!/usr/bin/python3
#
# Script Name: get_max_id_num.py
# Location   : /home/louis/Development/python/mymoney
# Description: This script returns the largest security ID number assigned
#              in the "mymoney" collection of the MongoDB.
#
# Developer: Louis Lao
# Date: Nov 13, 2016
#
# Modified By: Louis Lao
# Date: Oct 26, 2017
# Reason: The MongoDB access authorization class is now in a separate
#         module (auth_mongodb.py). Add import statement.

import auth_mongodb
import moneyMod1

# Access to MongoDB instance with authentication. (Administrator access)
#uri = "mongodb://admin:LLadmin8@localhost:27017/admin?authMechanism=SCRAM-SHA-1"
# User access.
hostDB = auth_mongodb.MongoDB_Login ("localhost", "27017",
           "money_user", "LLadmin8", "mymoney")
userDB = hostDB.connect_via_uri ()
qry = moneyMod1.Queries_Money (userDB)

num = qry.get_max_id_num ()

print ("The largest ID number used so far is", num)

