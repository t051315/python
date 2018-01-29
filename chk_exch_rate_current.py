#!/usr/bin/python3
#
# Script Name: chk_exch_rate_current.py
# Location   : /home/louis/Development/python/mymoney
# Description: This script scrapes almost real-time exchange rate data from
#              the Bloomberg finance site.
#
# Developer: Louis Lao
# Date: May 16, 2017
#
# Modified By:
# Date:
# Reason:

import moneyMod1

# Scrape data to get canadian to USD currency exchange rate.
url = "https://www.bloomberg.com/markets/currencies"
exchrate_scraper = moneyMod1.Scraper (url, True)

# Scrape the current exchange rate data - date and quote.
rateData = exchrate_scraper.get_exchRate_current ()
rateData = rateData.split ("::")

print ("Quote date/time:", rateData[0])
print ("Quote: %6.4f (%6.4f)" % (float(rateData[1]), (1.0/float(rateData[1])) ) )

print ()
input ("Press Enter to exit.")

