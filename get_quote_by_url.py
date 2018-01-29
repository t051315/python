#!/usr/bin/python3
#
# Script Name: get_quote_by_url.py
# Description: Script to scrape "quote" data from financial web pages defined
#              by given url(s).
#
# Developer: Louis Lao
# Date: Mar 9, 2017
#
# Modified By: Louis Lao
# Date: Oct 26, 2017
# Reason: The MongoDB access authorization class is now in a separate
#         module (auth_mongodb.py). Add import statement.

import sys
import auth_mongodb
import moneyMod1     # Custom module for "mymoney" web app. 

# Set the variable to the security ID you want to add latest quote to with data
#  scraped from the web.
#url = "http://www.theglobeandmail.com/globe-investor/funds-and-etfs/funds/summary/?id=87477"
#url = "https://finance.google.ca/finance?cid=675094"
#url = "https://www.theglobeandmail.com/globe-investor/markets/stocks/analysts/?q=T-T"
#url = "http://www.theglobeandmail.com/globe-investor/funds-and-etfs/funds/summary/?id=60101"
url = "https://www.theglobeandmail.com/globe-investor/markets/stocks/analysts/?q=IXJ-N"
url = "https://www.theglobeandmail.com//globe-investor/funds-and-etfs/funds/summary/?id=57936"

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

# Get quote data for the specified security.
try:
  quote_data = qry.get_fund_quote_by_URL (url)
#quote_data = qry.get_stock_quote_by_URL (url)
except Exception as e:
  # Error detected when scraping financial data from the given page.
  print ("  Operation failed! Error detected .. message  is ", e)
else:
  # Valid data collected.
  print (quote_data)

print ()
quit()
