#!/usr/bin/python3
#
# Script Name: chk_quotes_by_qry.py
# Description: This script is crudely adapted from 'quotes_add.py' which 
#              collects all the quote data for all our investments. This
#              however will only retrieve quote data for a small subset
#              of the securities in the database, depending on the query,
#              even down to one. This is designed to provide detailed
#              information to help check data when a security is found to
#              have some problems.
#
# Developer: Louis Lao
# Date: Jun 29, 2016
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
# Date: Dec 11, 2017
# Reason: For stocks or bonds that are quoted in USD but are reported to us
#         converted to CAD, I have coded to deal with that by multiplying
#         it by the current exchange rate. I modify the report to show both
#         original quote in USD and the converted quote in CAD together.


import sys
import re

import auth_mongodb
import moneyMod1


# Get access to the "mymoney" database.
hostDB = auth_mongodb.MongoDB_Login ("localhost", "27017",
           "money_user", "LLadmin8", "mymoney")
userDB = hostDB.connect_via_host ()
qry = moneyMod1.Queries_Money (userDB)

# Prepare the query filter to retrieve the security/ies you want to
#  check.
flt_docs = { "security_id":8 }
flt_docs = { "security_name": re.compile(r"edgepoint", re.IGNORECASE) }
flt_docs = { "security_name": re.compile(r"shares", re.IGNORECASE) }
cursor = qry.get_security_quote_by_qry (flt_docs)

# Scrape data to get canadian to USD currency exchange rate.
url_rate = "http://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/"
exchrate_scraper = moneyMod1.Scraper (url_rate, True)
exch_rate = exchrate_scraper.get_exchRate ()

counter = 0
for item in cursor:
  counter = counter + 1
  print ("\n" + str(counter) + ") Looking up " + item["security_name"] + ":")

  if item["security_type"] == 'fund':
    # Get quote data for the specified security.
    try:
      data = qry.get_fund_quote_by_URL (item["security_url"])
    except Exception as e:
      # Error detected when scraping financial data from the given page.
      print ("   *********Error detected...", e)
      continue

  else:
    # This security is a stock. Unfortunately I cannot find a site
    #  that would give me all the data I want. I need to go to two
    #  sites to get them - Globe & Mail and Google.
    #
    # And in this case,the variable 'item["security_url"]' actually
    #  contains the two sites' URLs, and I need to break it up.
    try:
      data = qry.get_stock_quote_by_URL (item["security_url"])
    except Exception as e:
      # Error detected when scraping financial data from the given page.
      print ("   *********Error detected...", e)
      #print ("   Error detected .. message  is ", e)
      continue

  # If the quoted price is in USD, then I want to convert it to
  #  CAD before saving it to the database. The attribute "currency'
  #  appears only in the database when it is needed.
  try:
    if (item["currency"]):
      # Currency is not in CAD. Convert it.
      converted = float(data["price"]) * exch_rate
      data["price"] = data["price"] + "/$" + str(round(converted, 4))
      #data["price"] = str(round(converted, 4))

  except KeyError as e:
    pass

  print ( "   " + data["name"] + " (As on " + data["date"] + ", the price is $" +
          data["price"] + ". YTD Change is " + data["ytd_chg"] + ")" )

print ()
quit()

