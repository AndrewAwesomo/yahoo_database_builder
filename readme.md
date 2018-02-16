Creates a database of daily adjusted prices from Yahoo finance from a batch list of ticker symbols.  See the included russell3000.txt for an example.  The symbols are assumed to be the last word in each line and all uppercase.  You can also use a file where the ticker is the only word per line, but tickers must be delimited by a new line.

This script requires the yqd.py module by c0redumb from https://github.com/c0redumb/yahoo_quote_download

This module is included and should be in the same directory as the .py file (i.e. a_01_BuildStockDatabase.py) that imports it.

Output is a new sqlite3 database with a table for each ticker, formatted with an underscore before the ticker symbol ex: Apple, ticker AAPL will have a table called ‘_AAPL’

A new file called report.txt is generated which lists the tickers that were unable to be downloaded from yahoo finance as well as a report on how long the batch download took to complete.
