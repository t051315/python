#!/usr/bin/python3
#
# Script Name: security_add.py
# Description: This script adds a new security into the "mymoney" collection
#              of the MongoDB.
#
# Developer: Louis Lao
# Date: Jun 29, 2016
#
# Modified By: Louis Lao
# Date: Oct 26, 2017
# Reason: The MongoDB access authorization class is now in a separate
#         module (auth_mongodb.py). Add import statement.
#
# Modified By: Louis Lao
# Date: Dec 04, 2017
# Reason: Globe and Mail does not provide Year-To-Date percent change for
#         stocks. Remove reference to it.

import auth_mongodb
import moneyMod1


# Access to MongoDB instance with authentication. (Administrator access)
#uri = "mongodb://admin:LLadmin8@localhost:27017/admin?authMechanism=SCRAM-SHA-1"
# User access.
hostDB = auth_mongodb.MongoDB_Login ("localhost", "27017",
           "money_user", "LLadmin8", "mymoney")
userDB = hostDB.connect_via_uri ()
qry = moneyMod1.Queries_Money (userDB)


post = { "security_id": 58,
         "security_name": "Dell Technologies Inc",
         "security_type": "stock",
         "security_url": "https://finance.google.ca/finance?q=NYSE%3ADVMT&ei=EEL4V5HuH-fDigLjr5bACQ",
         "owners":["Elsie"],
         "prod_code":"NA",
         "quotes":[],
         "status": "active"
       }

qry.add_security (post)

