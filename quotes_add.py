#!/usr/bin/python3
#
# Script Name: quotes_add.py
# Location   : /home/louis/Development/python/mymoney
# Description: Script to load stock and fund quotes into the Mongo collection
#              for the list of stocks and funds in the collection by scraping
#              data off web sites. A separate collection is also used to store
#              the currency rates as well as TSX and Dow indexes.
#
# Developer: Louis Lao
# Date: Jun 28, 2016
#
# Modified By: Louis Lao
# Date: Dec 9, 2016
# Reason: There are two URLs to get all the quotes info for stocks, in contrast
#         to funds which only need one. The two URLS were separated by ";" and
#         now I found out that PyMongo chokes on the character. So now I must
#         used different string to indicate the separation, and I chose "^^".
#
# Modified By: Louis Lao
# Date: Mar 8, 2017
# Reason: Refactor code to scrape security financial data. Code now resides
#         in the common class in moneyMod1.py.
#
# Modified By: Louis Lao
# Date: Apr 29, 2017
# Reason: The Bank of Canada URL I accessed to extract US dollar exchange
#         rate from is changed, so I have to use the corrected URL.
#
# Modified By: Louis Lao
# Date: Oct 26, 2017
# Reason: The MongoDB access authorization class is now in a separate
#         module (auth_mongodb.py). Add import statement.
#
# Modified By: Louis Lao
# Date: Dec 02, 2017
# Reason: The Globe and Mail page that I scrape for TSX date and value is
#         found to be different both in URL and content. Modify code and
#         regex to accommodate the changes.
#
# Modified By: Louis Lao
# Date: Dec 30, 2017
# Reason: Add Bitcoin to be tracked like TSX and Dow Jones.


import sys

import auth_mongodb
import moneyMod1

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

# Scrape data to get canadian to USD currency exchange rate.
url = "http://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/"
exchrate_scraper = moneyMod1.Scraper (url)
exch_rate = exchrate_scraper.get_exchRate ()
print ("Exchange Rate: %6.4f (%6.4f)" % (exch_rate, 1.0/exch_rate) )

# Scrape quote date and value for TSX. The date is used as the date for
#  TSX as well as Dow Jones and exchange rate.
#url = "https://www.theglobeandmail.com/globe-investor/markets/"
url = "https://www.bloomberg.com/quote/SPTSX:IND"
indexes_scraper = moneyMod1.Scraper (url, False)
tsxData = indexes_scraper.get_dow_tsx ()
data = tsxData.split ("::")
idxDate = data[1]
tsx = data[2]
print ("Close date:", idxDate)

# Scrape Dow Jones index value.
#url = "http://www.marketwatch.com/investing/index/djia"
url = "https://www.bloomberg.com/quote/INDU:IND"
indexes_scraper = moneyMod1.Scraper (url, False)
dowData = indexes_scraper.get_dow_tsx ()
data = dowData.split ("::")
dow = data[2]

# Scrape Bitcoin value from Google site.
url = "https://finance.google.com/finance?q=currency:btc"
indexes_scraper = moneyMod1.Scraper (url, False)
btcData = indexes_scraper.get_bitcoin ()
data = btcData.split ("::")
btc = data[0]

print ("TSX:", tsx)
print ("Dow:", dow)
print ("Bitcoin:", btc)
print ()

# Get access to the "mymoney" database.
hostDB = auth_mongodb.MongoDB_Login ("localhost", "27017",
           "money_user", "LLadmin8", "mymoney")
userDB = hostDB.connect_via_host ()
qry = moneyMod1.Queries_Money (userDB)

if (upd == "upd"):
  # Add a new record in the "rates" collection with exchange rate and 
  #  TSX and Dow indexes.
  #  qry.add_indexes ( idxDate, exch_rate, indexes["tsx"], indexes["dow"])
  #  qry.add_indexes ( idxDate, exch_rate, tsx, dow )
  qry.add_indexes ( idxDate, exch_rate, tsx, dow, btc )

# Process all the active funds and stocks in our family's portfolios.
cursor = qry.get_security_quote_by_qry ({"status":"active"})

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
