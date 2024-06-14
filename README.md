# scraping

Scraping program. Notifies you when prices are lower on web sites or the stock price reaches a specified value.


### Usage

###### pc/dell.py

###### pc/lenovo.py

Scraping PC prices and saving them to a file.
Notify on line when the price information differs from the price information stored in the file.


###### stock/stock_checker.py

###### stock/tickers.csv

In the file "tickers.csv", determine the stocks, threshold values, and whether the target value is higher or lower than the target value.
The stock prices of the stocks in the csv file are checked and notified when the conditions are met.


Example of csv file (multiple lines can be specified)

| name                 | target | threshold | high_or_low |
| -------------------- | ------ | --------- | ----------- |
| Alphabet Inc Class A | GOOGL  | 170       | +           |
