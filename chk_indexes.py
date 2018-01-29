#!/usr/bin/python3
#
# Script Name: chk_indexes.py
# Location   : /home/louis/Development/python/mymoney
# Description: This script scrapes TSX and Dow indexes data from Globe
#              and Mail site. Data include the quote dates and index
#              values. This script will dump intermediate data to make
#              sure the data is correct.
#
# Developer: Louis Lao
# Date: Jun 29, 2016
#
# Modified By: Louis Lao
# Date: May 24, 2017
# Reason: I used to take the TSX and Dow indexes data entirely from Globe
#         and Mail site, and the quote date for TSX as the date/time for
#         both, which is not always correct. As I do not like Dow quote
#         date on the Globe site, I decide to extract Dow index data from
#         MarketWatch site instead.
#
# Modified By: Louis Lao
# Date: Dec 02, 2017
# Reason: The Globe and Mail page that I scrape for TSX date and value is
#         found to be different both in URL and content. Modify code and
#         regex to accommodate the changes.
#
# Modified By: Louis Lao
# Date: Dec 04, 2017
# Reason: Scrape TSX and DOW indices from practically identical pages from
#         Bloomberg.
#
# Modified By: Louis Lao
# Date: Dec 29, 2017
# Reason: Add Bitcoin to be tracked like TSX and Dow Jones.

import moneyMod1

# Get TSX data from Bloomberg web site.
#url = "https://www.theglobeandmail.com/globe-investor/markets/"
url = "https://www.bloomberg.com/quote/SPTSX:IND"
indexes_scraper = moneyMod1.Scraper (url, True)

print ("Getting TSX ......\n")

# Firstly get the quotes date/time for TSX.
tsxData = indexes_scraper.get_dow_tsx ()

data = tsxData.split ("::")
print ("TSX quote date detail:", data[0])
print ("TSX quote date:", data[1])
print ("TSX:", data[2])
print ("TSX 1 Day Change:", data[3])
print ( )
print ( )

# Get Dow Jones data from Bloomberg web site.
#url = "http://www.marketwatch.com/investing/index/djia"
url = "https://www.bloomberg.com/quote/INDU:IND"
indexes_scraper = moneyMod1.Scraper (url, True)

print ("Getting DOW ......\n")

# Firstly get the quotes date/time for Dow Jones.
dowData = indexes_scraper.get_dow_tsx ()

data = dowData.split ("::")
print ("Dow quote date detail:", data[0])
print ("Dow quote date:", data[1])
print ("Dow:", data[2])
print ("DOW 1 Day Change:", data[3])
print ( )
print ( )

# Get Bitcoin data from Google web site. 
url = "https://finance.google.com/finance?q=currency:btc"
indexes_scraper = moneyMod1.Scraper (url, True)

print ("Getting Bitcoin (From Google) ......\n")

# Firstly get the quotes date/time for Bitcoin.
btcData = indexes_scraper.get_bitcoin ()

data = btcData.split ("::")
print ("Bitcoin date detail:", data[3], data[5], data[6])
print ("Bitcoin quote date:", data[3])
print ("Bitcoin:", data[0])
print ("Bitcoin Change:", data[1])
print ("Bitcoin % Change:", data[2])
print ( )

input ("Press Enter to exit.")

