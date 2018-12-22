#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 17:32:44 2018

@author: colleencallahan
"""

"""
Here we find all the csv files in our working directory that correspond with the stock data. We then read in all the csv files and concatenate them into one data frame. We add a column with the ticker symbol corresponding with that stock.
"""

import pandas as pd # Load pandas as pd
import glob # Import glob

files = glob.glob('*.csv') # Find all the files in wd that end in .csv

df = pd.DataFrame() # Create a data frame
for file in files: # For each file
    newdf = pd.read_csv(file) # Read in the data and create a dataFrame with data
    newdf['Ticker'] = file.replace('.csv', '') # Add a column with the Ticker symbol
    df = pd.concat([df,newdf]) # Add this data to the big DataFrame
    
"""
Here we find the mean price for categories Open, High, Low, Close.
"""

group = df.loc[:,'Open':'Close'] # Extract the columns Open, High, Low, Close
group.mean() # Find the mean price for each group


"""
Then we group by the ticker symbol and find the mean close price. We then index on the top 5 and the bottom 5 mean close price.
"""

group1 = df['Close'].groupby(df['Ticker']) # Group the Close price by each stock ticker
top5 = group1.mean().sort_values()[0:5] # Sort the mean values and find the top 5
bottom5 = group1.mean().sort_values()[-5:] # Sort the mean values and find the bottom 5

"""
We add the feature Volatility, or the difference between high and low stock prices. We find the top 5 volatility stocks and bottom 5 volatility stocks 
""" 

df['Volatility'] = df['High'] - df['Low'] # Add a column to dataFrame with Volatility

group2 = df['Volatility'].groupby(df['Ticker']) # Group Volatility by ticker symbol
top5 = group2.mean().sort_values()[0:5] # Sort the mean values and find top 5 volatility
bottom5 = group2.mean().sort_values()[-5:] # Sort the mean values and find bottom 5 volatility


"""
We now engineer a new feature, relative volatility. We can find the top 5 and bottom 5 relative volatility stocks, as well. 
"""
df['Relative Volatility'] = (df['High'] - df['Low'])/(0.5*(df['Open'] + df['Close'])) # Add a column to the dataFrame with Relative Volatility

group3 = df['Relative Volatility'].groupby(df['Ticker']) # Group relative volatility by ticker symbol
top5 = group3.mean().sort_values()[0:5] # Sort the mean values and find top 5 volatility
bottom5 = group3.mean().sort_values()[-5:] # Sort the mean values and find bottom 5 volatility

"""
We convert the date column to datetime format. Then we can index on the date and find the mean of each open, low, high, and close prices from specific dates. In this case we use Feb 2010.
"""

df['Date'] = pd.to_datetime(df['Date']) # Convert Date column to datetime 
feb = df[df['Date'].dt.month == 2] # Extract all entries from february
feb2010 = feb[feb['Date'].dt.year == 2010] # Extract all entries from february 2010
group4 = feb2010.loc[:,'Open':'Close'] # Extract Open, Low, High, Close Prices from feb 2010

group4.mean() # Find the mean of each Open, Low, High, Close from feb 2010

"""
Next we find the relative volatilities for each date from 2012. Then we find the dates from 2012 with the max average volatility and the min average volatility.
""" 

df['Date'] = pd.to_datetime(df['Date']) # Convert Date column to datetime
y12 = df[df['Date'].dt.year == 2012] # Extract all entries from 2012
date12 = y12.groupby(y12['Date']) # Group entries from 2012 by Date
relvol = date12.mean()['Relative Volatility'] #Find the average relative volatilites for each date from 2012
min = relvol[relvol == relvol.min()] # Find the Date with the minimum average volatility 
max = relvol[relvol == relvol.max()] # Find the Date with the maximum average volatility 


"""
After grouping by day of the week, we are able to find the avg relative volatility for each day of the week.
"""

dataframe = df[(df['Date'].dt.year >= 2008) & (df['Date'].dt.year <= 2013)] #Extract all entries from 2008-2013
group5 = dataframe.groupby(dataframe['Date'].dt.dayofweek) # Group by the day of th week
group5['Relative Volatility'].mean() # Find the average relative volatility for each day of the week

"""
Here we index on all the entries from october 2010 and create new features open, close, high, low with weights. WE can then find the python index by the sum of each weighted column by the volume.
"""


oct = df[df['Date'].dt.month == 10] # Extract all entries from october
oct10 = oct[oct['Date'].dt.year == 2010] # Extract all entries from october 2010

oct10['Weighted Open'] = oct10['Open'] * oct10['Volume'] # Compute weighted open prices by multiplying open by volume
oct10['Weighted Close'] = oct10['Close'] * oct10['Volume']# Compute weighted close prices by multiplying close by volume
oct10['Weighted High'] = oct10['High'] * oct10['Volume'] # Compute weighted high prices by multiplying high by volume
oct10['Weighted Low'] = oct10['Low'] * oct10['Volume'] # Compute weighted low prices by multiplying low by volume


group6 = oct10.loc[:,'Weighted Open':'Weighted Low'].groupby(oct10['Date']) # Group each weighted open, close, low, high by the date 
group7 = oct10['Volume'].groupby(oct10['Date']) # Group volume by each date 

pythonindex = group6.sum().divide(group7.sum(), axis='index') # Compute the python index by dividing the sum of each weighted column by the sum of volume


"""
We can find the number of days the stock market was open from 2005 to 2014 by finding the number of unique dates within that time frame.
"""

df['Date'] = pd.to_datetime(df['Date']) # Convert Date column to datetime
dataframe = df[(df['Date'] >= '2005-1-2') & (df['Date'] <= '2014-12-31')] # Extract the entries from January 2, 2005 to Decemeber 31, 2014


opendates = dataframe['Date'].drop_duplicates() # Find the unique dates where the market was open from 2005 to 2014
openyears = opendates.dt.year # Extract the years from 2005 to 2014
opencount = openyears.value_counts() # Count the number of entries from each year
opencount.sort_index() # Sort by year 


"""
Here we find the number of missing records.
"""


tickers = dataframe['Ticker'].drop_duplicates() # Find the unique ticker symbols
tickerlist = tickers.tolist() # Convert to a list

no_missing_date = pd.Series() # Create an empty series
ndf = pd.DataFrame() # Create an empty dataframe
for x in tickerlist: # For each ticker symbol in the tickerlist
    ids = df['Date'][df['Ticker'] == x] # Mask on the dates for that particular stock
    start_date = ids.min() # Find the date where the data starts
    end_date = ids.max() # Find the date where the data ends 
    opennew = opendates[(opendates >= ids.min()) & (opendates <= ids.max())] # Mask on dates when market was open for the dates that the stock has records
    datelist = ids.tolist() # Put these open dates into a list
    missing = opennew[~opennew.isin(datelist)] # Find the missing dates from the particular stock
    ddf = pd.DataFrame(missing) # Put the missing dates into a dataframe
    ddf['Ticker'] = x # Add the ticker symbol for the sock to the dataframe
    if len(missing) == 0: # If there are no missing records
        no_missing_date[x] = 0 # Add to the series that has no missing records
    else: #If there are missing records
        ndf = pd.concat([ndf,ddf]) # Concatenate with the larger dataframe
ndf = ndf[(ndf['Date'] >= '2005-1-2') & (ndf['Date'] <= '2014-12-31')] # Mask the dates that are between Jan 2 2005 and Dec 31 2014

 num_missing_records = len(ndf) # Find the length of the dataframe to get the number of missing records


"""
Next, we find the dates that had no missing records and the most missing records.
"""


newdata = ndf.groupby(ndf['Ticker']) # Group the missing records by stock
count_missing_records = newdata.count() # Count the missing records for each stock
missingstock = count_missing_records['Date'].sort_values() # Sort the values 
bottom_10 = no_missing_date # Find the dates that had no missing records (10 stocks with least missing records)
top_10 = missingstock[-14:] # Find the dates that had the most missing records (with ties)


"""
Then, we calculate the proportion of missing records for each stocks and find the specific stocks with the highest and lowest proportion of missing stocks, respectively. 
"""

givenrecords = dataframe['Date'].groupby(dataframe['Ticker']).count() # Count the number of records given for each stock
missing_records = pd.concat([count_missing_records['Date'], no_missing_date]) # Concatenate the series of missing records and stocks that had no missing records 
prop = missing_records / (givenrecords + missing_records) # Calculate the proportion of missing records for each stock

prop = prop.sort_values() # Sort the proportions of missing records
prop[-15:] # Find the stocks with the highest proportion of missing records
prop[0:10] # Find the stocks with the least proportion of missing records 


"""
 Then we can find the top 10 dates with the most missing records.
"""


missing_dates = ndf.groupby(ndf['Date']) # Group missing records by date
values = missing_dates.count()['Ticker'].sort_values(ascending=False) # Count the number of stocks that had missing records for each date
values[0:10] # Find the top 10 dates with the most missing records


"""
Here we impute the values of dates that have missing values. We add these to the dataframe.
"""
 


ndf = ndf.reset_index(drop=True) # Reset the indices for the dataframe with missing dates
newdataframe = pd.DataFrame() # Create an empty dataframe
for i in range(len(ndf)): # For entry in the dataframe of missing dates
    object = ndf.iloc[i] # Extract the entry with date and ticker symbol
    md = object['Date'] # Isolate the missing date
    mt = object['Ticker'] # Isolate the ticker symbol of the stock

    stock = df[df['Ticker'] == mt] # Mask on the dataframe with all the records to extract the records for only this particular stock
    stockbelow = stock[stock['Date'] < md].max() # Mask all the entries below the missing date and find the max to find date below
    stockabove = stock[stock['Date'] > md].min() # Mask all the entries aboce the missing date and find the max to find date above
    
    openprice = ((stockabove['Date'] - md).days * stockbelow['Open']) + ((md - stockbelow['Date']).days * stockabove['Open']) / (stockabove['Date'] - stockbelow['Date']).days # Compute the impute open price for the missing date
    closeprice = ((stockabove['Date'] - md).days * stockbelow['Close']) + ((md - stockbelow['Date']).days * stockabove['Close']) / (stockabove['Date'] - stockbelow['Date']).days # Compute the imputed close price for the missing date 
    highprice = ((stockabove['Date'] - md).days * stockbelow['High']) + ((md - stockbelow['Date']).days * stockabove['High']) / (stockabove['Date'] - stockbelow['Date']).days # Compute the imputed high price for the missing date
    lowprice = ((stockabove['Date'] - md).days * stockbelow['Low']) + ((md - stockbelow['Date']).days * stockabove['Low']) / (stockabove['Date'] - stockbelow['Date']).days # Compute the imputed low price for the missing date
    volume = ((stockabove['Date'] - md).days * stockbelow['Volume']) + ((md - stockbelow['Date']).days * stockabove['Volume']) / (stockabove['Date'] - stockbelow['Date']).days # Compute the imputed volume or the missing date
    missingtick = [mt] # Create a list with the ticker symbol of this particular stock
    newdf1 = pd.DataFrame({'Ticker': missingtick}) # Create a new dataframe with this ticker symbol
    newdf1['Date'] = md # Add the missing date to dataframe
    newdf1['Open'] = openprice # Add the imputed open price
    newdf1['Close'] = closeprice # Add the imputed close price
    newdf1['High'] = highprice # Add the imputed high price
    newdf1['Low'] = lowprice # Add the imputed volume
    newdataframe = pd.concat([newdataframe, newdf1]) # Concatenate this with the larger dataframe
newdataframe


oct = newdataframe[newdataframe['Date'].dt.month == 10] # Extract all entries from october from imputed values dataframe
oct10 = oct[oct['Date'].dt.year == 2010] # Extract all entries from october 2010

oct10['Weighted Open'] = oct10['Open'] * oct10['Volume'] # Compute weighted open prices by multiplying open by volume
oct10['Weighted Close'] = oct10['Close'] * oct10['Volume']# Compute weighted close prices by multiplying close by volume
oct10['Weighted High'] = oct10['High'] * oct10['Volume'] # Compute weighted high prices by multiplying high by volume
oct10['Weighted Low'] = oct10['Low'] * oct10['Volume'] # Compute weighted low prices by multiplying low by volume


group6 = oct10.loc[:,'Weighted Open':'Weighted Low'].groupby(oct10['Date']) # Group each weighted open, close, low, high by the date 
group7 = oct10['Volume'].groupby(oct10['Date']) # Group volume by each date 

pythonindex = group6.sum().divide(group7.sum(), axis='index') # Compute the python index by dividing the sum of each weighted column by the sum of volume

"""
Then, we find the mean python index for each month of each year from 2008 to 2012.
"""

 

newyear = newdataframe[(newdataframe['Date'].dt.year >= 2008 ) & (newdataframe['Date'].dt.year <= 2012)] # Mask on new dataframe to extract imputed values from 2008 to 2012


newyear['Weighted Open'] = newyear['Open'] * newyear['Volume'] # Compute weighted open prices by multiplying open by volume
newyear['Weighted Close'] = newyear['Close'] * newyear['Volume']# Compute weighted close prices by multiplying close by volume
newyear['Weighted High'] = newyear['High'] * newyear['Volume'] # Compute weighted high prices by multiplying high by volume
newyear['Weighted Low'] = newyear['Low'] * newyear['Volume'] # Compute weighted low prices by multiplying low by volume


group6 = newyear.loc[:,'Weighted Open':'Weighted Low'].groupby(newyear['Date']) # Group each weighted open, close, low, high by the date 
group7 = newyear['Volume'].groupby(newyear['Date']) # Group volume by each date 

pythonindex = group6.sum().divide(group7.sum(), axis='index') # Compute the python index by dividing the sum of each weighted column by the sum of volume
pythonindex['Dates'] = pythonindex.index # Add a column with the dates for each python index
group = pythonindex.groupby([pythonindex['Dates'].dt.year, pythonindex['Dates'].dt.month]) # Group by the month and the year for each python index
group.mean() # Find the mean python index each month of each year


