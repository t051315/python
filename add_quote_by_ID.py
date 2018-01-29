#!/usr/bin/python3
#
# Script Name: add_quote_by_ID.py
# Location   : /home/louis/Development/python/mymoney
# Description: Script to add the latest quote to a specific security given by
#              its database ID. The purpose is to populate the new security 
#              which has been created in the database with a blank array of
#              quotes with a set of the latest quote values. Because with an
#              empty array, a few web reports will produce errors.
#
#              ( Please also check sister script:
#                  /var/www/cgi-bin/python/mymoney/add_quote_by_id.py )
#
# Developer: Louis Lao
# Date: Feb 18, 2017
#
# Modified By: Louis Lao
# Date: Mar 8, 2017
# Reason: Refactor code to scrape security financial data. Code now resides
#         in the common class in moneyMod1.py.
#
# Modified By: Louis Lao
# Date: Oct 26, 2017
# Reason: The MongoDB access authorization class is now in a separate
#         module (auth_mongodb.py). Add import statement.
#
# Modified By: Louis Lao
# Date: Dec 02, 2017
# Reason: Changes to description and comments.

import sys
import auth_mongodb
import moneyMod1

# Set the variable to the security ID you want to add latest quote to with data
#  scraped from the web.
target_id = 17

# Check the paramter whether the user wants to update the quotes
#  into the database or not. This option parameter must be present.
if len(sys.argv) <= 1 :
  print ("Argument missing!")
  print ("Usage: " + sys.argv[0] + 
      " upd/noupd (upd - update to database; noupd - no updates)")
  sys.exit(2)

elif len(sys.argv) > 2 :
  print ("Too many arguments!")
  print ("Usage: " + sys.argv[0] +
      " upd/noupd (upd - update to database; noupd - no updates)")
  sys.exit(2)

else :
  # This indicates that there is just one option on the command
  #  line, which is expected. Then I check whether is it one of
  #  two acceptable options.
  if (sys.argv[1] == "upd") or (sys.argv[1] == "noupd"):
    upd = sys.argv[1]

  else :
    print ("Wrong arguments!")
    print ("Usage: " + sys.argv[0] + " upd/noupd")
    sys.exit(2)

# Get access to the "mymoney" database.
hostDB = auth_mongodb.MongoDB_Login ("localhost", "27017",
           "money_user", "LLadmin8", "mymoney")
userDB = hostDB.connect_via_host ()
qry = moneyMod1.Queries_Money (userDB)

# Get quote data for the specified security.
cursor = qry.get_security_quote_by_qry ({"security_id":target_id})

# Scrape data to get canadian to USD currency exchange rate.
url_rate = "http://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/"
exchrate_scraper = moneyMod1.Scraper (url_rate)
exch_rate = exchrate_scraper.get_exchRate ()

# Note that there is only one document returned.
for item in cursor:
  print ("\n   Looking up " + item["security_name"] + ":")

  if item["security_type"] == 'fund':
    # Get quote data for the specified mutual fund.
    try:
      data = qry.get_fund_quote_by_URL (item["security_url"])  
    except Exception as e:
      # Error detected when scraping financial data from the given page.
      print ("   *********Error detected...", e)
      continue

  else:
    # Get quote data for the specified stock.
    try:
      data = qry.get_stock_quote_by_URL (item["security_url"])    
    except Exception as e:
      # Error detected when scraping financial data from the given page.
      print ("   *********Error detected...", e)
      continue

  # If the quoted price is in USD, then I want to convert it to
  #  CAD before saving it to the database. The attribute "currency'
  #  appears only when it is needed.
  try:
    if (item["currency"]):
      # Currency is not in CAD. Convert it.
      converted = float(data["price"]) * exch_rate
      data["price"] = str(round(converted, 4))

  except KeyError as e:
    pass

  print ( "   " + data["name"] + " (As on " + data["date"] + ", the price is $" +
          data["price"] + ". YTD Change is " + data["ytd_chg"] + ")" )

  if upd == "upd" :
    qry.add_quote ( item["security_id"], data["date"], data["price"], data["ytd_chg"] )

print ()
quit()

