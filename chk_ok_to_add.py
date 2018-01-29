#!/usr/bin/python3
#
# Script Name: chk_ok_to_add.py
# Location   : /home/louis/Development/python/mymoney
# Description: To reliably and accurately adding month-end securities closing
#              quotes into the database, I need to know that all of them have
#              identical targeted closing date. This script will check each
#              security closing quote date to match a given targeted date to
#              be entered manually as a parameter on the command line, which
#              is normally the last working date of the month. The output is
#              a message whether it is OK to add the quotes to the database,
#              or wait until all the dates are identical.
#
# Developer: Louis Lao
# Date: May 21, 2017
#
# Modified By: Louis Lao
# Date: May 24, 2017
# Reason: Add TSX index quote date to be checked.
#
# Modified By: Louis Lao
# Date: Oct 26, 2017
# Reason: The MongoDB access authorization class is now in a separate
#         module (auth_mongodb.py). Add import statement.
#
# Modified By: Louis Lao
# Date: Dec 02, 2017
# Reason: The URl for the Globe and Mail page where I scrape TSX data from is
#         changed.

import sys
import re
import datetime

import auth_mongodb
import moneyMod1

# Make sure that there is one and only one parameter on the command line and
#  that it is in a valid date format (YYYY-MM-DD).
if len(sys.argv) <= 1 :
  print ("Argument missing!")
  print ("Usage: " + sys.argv[0] + " (a date in the following format: 2017-04-24)")
  sys.exit(2)

elif len(sys.argv) > 2 :
  print ("Too many arguments!")
  print ("Usage: " + sys.argv[0] + " (a date in the following format: 2017-04-24)")
  sys.exit(2)

else :
  # Now make sure that the parameter given is in a date format and it is valid.
  re_date = re.compile (r'(20\d{2})-(\d{2})-(\d{2})')
  match = re_date.match (sys.argv[1])
  if match :
    # The parameter is verified to be in an acceptable date format. Now check
    #  if it is a valid date.
    try :
      dt = datetime.datetime (int(match.group(1)), int(match.group(2)), int(match.group(3)))

    except ValueError :
      print ("Date given is not valid! Try again.")
      sys.exit(2)

  else :
    print ("Wrong date format!")
    print ("Date must be in the following format: 2017-04-24")
    sys.exit(2)

target_date = match.group(0)

# Because TSX index, Dow Jones index and exchange rate may have different
#  dates, therefore I have to choose one date as the date for all of them.
#  And since the "mymoney" database is Canadian based, I choose the quote
#  date for TSX index as the common date for the database. This date is
#  extracted from Globe and Mail financial web site.
#url = "https://www.theglobeandmail.com/globe-investor/markets/"
url = "https://www.bloomberg.com/quote/SPTSX:IND"
idxDate_scraper = moneyMod1.Scraper (url, False)
idxDate = idxDate_scraper.get_dow_tsx ()
data = idxDate.split ("::")
idxDate = data[1]

if (idxDate != target_date ):
  print ("TSX/Dow indexes and exchange rate date (" + idxDate + ") is bad. Exiting now.")
  print ( )
  sys.exit (2)


# Once the indexes and exchange rate date is validated, then the rest of
#  the checking process can proceed.
#
# Get access to the "mymoney" database.
hostDB = auth_mongodb.MongoDB_Login ("localhost", "27017",
           "money_user", "LLadmin8", "mymoney")
userDB = hostDB.connect_via_host ()
qry = moneyMod1.Queries_Money (userDB)

# Process all the active funds and stocks in our family's portfolios.
cursor = qry.get_security_quote_by_qry ({"status":"active"})

good = 0
bad  = 0

badlist = []

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
      continue
    
  print ( "     Quote Date: " + data["date"], end='' )

  if ( data["date"] == target_date ) :
    print ( " (GOOD!)" )
    good += 1

  else :
    print ( " (BAD!)" )
    bad += 1
    badlist.append ("(" + str(counter) + ") " + data["name"])

print ( )
print ("Total number of securities: " + str(counter))
print ("Number of goods: " + str(good) + " and the number of bads: " + str(bad))

print ("List of bad:\n")
for bad in badlist :
  print ( " ", bad)

print ()
quit()

