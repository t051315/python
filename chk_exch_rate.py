#!/usr/bin/python3
#
# Script Name: chk_exch_rate.py
# Location   : /home/louis/Development/python/mymoney
# Description: This script is crudely adapted from 'quotes_add.py' which,
#              as its main job to collect all the quote data for all our
#              investments, also retrieves the Canadian to US currency
#              exchange rate. This script will dump intermediate data to
#              make sure the data is correct.
#
# Developer: Louis Lao
# Date: Jun 29, 2016
#
# Modified By: Louis Lao
# Date: Apr 29, 2017
# Reason: The Bank of Canada URL I accessed to extract US dollar exchange
#         rate from is changed, so I have to use the corrected URL.
#
# Modified By: Louis Lao
# Date: May 14, 2017
# Reason: Get the close date for the exchange rate for the report.

import os
import moneyMod1

# Scrape data to get canadian to USD currency exchange rate.
url = "http://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/"
exchrate_scraper = moneyMod1.Scraper (url, True)

rateDate = exchrate_scraper.get_rateDate ()
print ("Close date:", rateDate)

exch_rate = exchrate_scraper.get_exchRate ()
exch_rate_inverse = 1.0/exch_rate
print ("Exchange Rate: %6.4f (%6.4f)" % (exch_rate, exch_rate_inverse) )

print ()
input ("Press Enter to exit.")

