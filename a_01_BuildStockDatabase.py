# Builds a database with daily Adjusted Price data from Yahoo Finance

import sqlite3
import time
import yqd

TICKER_LIST='russell3000.txt' # name of file containing ticker list
DB_NAME='russell3000.db'  # name of database to create
# note that this is using unix time stamp so earliest start date is Jan 1, 1970
START_DATE='19700101'
END_DATE='20300101'


def updateDB(allTickers):
    t1 =time.clock()
    bad_tickers = []
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    count = 1
    for ticker in allTickers:
        print('%d of %d - writing %s to database' %(count, len(allTickers), ticker))
        error = create_table(ticker, c)
        if error != None:
            bad_tickers.append(error)
        count = count+1
    print(bad_tickers)
    t2=time.clock()
    total_time_s = str(t2-t1)
    total_time_h = str((t2-t1)/3600)
    report = open('report.txt', 'w')
    report.write('\n'.join(bad_tickers))
    report.write('\n total time %s seconds' %(total_time_s))
    report.write('\n or %s hours' %(total_time_h))
    report.close()

def create_table(ticker, c):
    ticker_data = get_ticker_data(ticker)
    if isinstance(ticker_data, str):
        print('failed to download ticker data')
        return ticker_data
    else:
        c.execute('CREATE TABLE IF NOT EXISTS %s(date TEXT PRIMARY KEY, adj_close FLOAT)' %('_' + ticker))
        for record in ticker_data:
            try:
                c.execute("INSERT INTO %s(date, adj_close) VALUES(?, ?)" %('_' + ticker), (str(record[0]), record[5]))
            except:
                print("failed to write to database")

def get_ticker_data(ticker):
    try:
        ticker_data = yqd.load_yahoo_quote(ticker, START_DATE, END_DATE)
        ticker_data.pop()  # get rid of blank string at end of data
        ticker_data = [row.split(',') for row in ticker_data]
        return ticker_data

    except:
        try:
            time.sleep(2) #delay 2 seconds and try again
            ticker_data = yqd.load_yahoo_quote(ticker, '19700101', '20300101')
            ticker_data.pop()  # get rid of blank string at end of data
            ticker_data = [row.split(',') for row in ticker_data]
            return ticker_data
        except:
            return ticker

def parseRus():
    # Returns a list of tickers from the Russell 3000 text file
    # Assumes last word in each line is ticker, and all tickers are uppercase
    # russell3000.txt is an example file
    # can also be used with files that only have a ticker on each line

    tickers = []
    readFile = open(TICKER_LIST, 'r').read()
    splitFile = readFile.split('\n')
    for eachLine in splitFile:
        splitLine = eachLine.split(' ')
        if splitLine[-1].isupper():
            tickers.append(splitLine[-1])
    return tickers

allTickers = parseRus()

updateDB(allTickers)
