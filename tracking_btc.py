#!/usr/bin/python3
#
# Script Name: tracking_btc.py
# Location   : /home/louis/Development/python/mymoney
# Description: This script scrapes
#
# Developer: Louis Lao
# Date:
#
# Modified By:
# Date:
# Reason:

import auth_mongodb
import moneyMod1

import datetime
import threading

# The following imports are required to trap Ctr-C to stop the script
#  without printing a bunch of error messages.
import signal
import sys
import os

def signal_handler (signal, frame) :
  print('\tExiting script because you pressed Ctrl+C!')
  sys.exit(0)

# Register the Ctr-C siganl handler. 
signal.signal (signal.SIGINT, signal_handler)
dev_null = open (os.devnull, 'w')
sys.stderr = dev_null
print('Press Ctrl+C to stop script!')

# Get Bitcoin data from Google web site. 
url = "https://finance.google.com/finance?q=currency:btc"

def scrape_btc () :
  timer = threading.Timer (90.0, scrape_btc)
  timer.start()
  indexes_scraper = moneyMod1.Scraper (url, False)
  btcData = indexes_scraper.get_bitcoin ()
  data = btcData.split ("::")
  print ("Taken at:", datetime.datetime.now().time())
  print ("Bitcoin date:", data[3], data[5], data[6])
  print ("Bitcoin:", data[0], "(" + data[1] + "/" + data[2] + ")")
  print ("Bitcoin BASE:", str(round((float(data[0]) - float(data[1])), 4)))
  print('Press Ctrl+C to stop script!')

if __name__ == "__main__" :
  scrape_btc()
