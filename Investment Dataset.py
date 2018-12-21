#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 17:34:02 2018

@author: colleencallahan
"""
"""
Here we use a function to calculate the balance of an investment after 25 years
"""

import numpy as np # Load numpy as np
import pandas as pd # Load pandas as pd
import matplotlib.pyplot as plt # Load matplot as plt


mu = 0.076 # Initialize mu
B_init = 50000.00 # Intialize balance
table = pd.DataFrame() # Create an empty dataframe
for x in range(40,66): # For x in years
    year = [x] # Create a list with the year
    df = pd.DataFrame(index = year) # Rename the index with the year
    df['Investment'] = B_init # Add the balance to the dataframe
    table = pd.concat([table, df]) # Concatenate with the big dataframe
    B_init = B_init*(np.exp(mu)) # Compute the next balance with the fixed rate     return 
table = np.round(table, 2) # Round the values to two decimal places

table.iloc[-1] # Find the balance on the 65th birthday


"""
Here we create 100000 simulations of the function that calculates the balance of investment after 25 years. We then find the mean and median, as well as the confidence interval of the 100000 simulations. We then plot a histogram of the 100000 final balances, one from each simulation. 
"""
lognormval = np.zeros(100000) # Create an array with zeroes 
for i in range(100000): # For the simulation in 10,000 simulations
    values = np.zeros(26) # Create an array with zeroes
    mu = 0.076 # Initialize mu
    sigma = 0.167 # Initialize sigma
    B_init = 50000.00 # Initialize the balance
    for j in range(26): # For j in years
        values[j] = B_init # Add the current balance to the array
        B_init = B_init*(np.exp(np.random.normal(mu, sigma))) # Compute the balance with lognormal distribution
    values = np.round(values, 2) # Round the values 
    tab = pd.Series(values, index=pd.Index(range(40,66))) # Add the values from birthday year 40 to 65 to a table
    lognormval[i] = tab.iloc[-1] # Add the 65th birthday to the array of 10000 simulations

## (a)

np.round(lognormval.mean(), 2) # Find the mean of the balances on his 65th birthday

##(b)

np.round(np.median(lognormval), 2) # Find the meadian of the balances on his 65th birthday


## (c)

lognormval.sort() # Sort the balances 
lognormval[2500:97501] # Find the 95% middle values 

ucl = lognormval[2500] # Find the upper confidence limit
lcl = lognormval[97500] # Find the lowere confidence limit

print([ucl, lcl]) # Print the confidence interval 

## (d)

success = lognormval[lognormval > 300000.00] # Mask on the investments greater than 300000
prop = len(success) / len(lognormval) # Find the proprotion of values greater than 30,000

## (e)

plt.hist(lognormval, bins=80, range=[0, 3000000]) # Plot the histogram 




"""
Here we find the balance of the investment after 25 years, when the investor makes a deposit of 3000 each year.
""" 
mu = 0.076 # Initialize mu
B_init = 50000.00 # Initialize the balance 
deposit = 3000 # Initialize the deposit
table1 = pd.DataFrame() # Create an empty data frame
for x in range(40,66): # For x in years
    year = [x] # Create a list with the year
    df = pd.DataFrame(index = year) # Rename the index with the year
    df['Investment'] = B_init # Add the balance to the dataframe
    table1 = pd.concat([table1, df]) # Concatenate with the big dataframe
    B_init = B_init*(np.exp(mu)) + deposit # Compute the new balance with the deposit 
table1 = np.round(table1, 2) # Round the values to two decimal places
table1.iloc[-1]

"""
We repeat the simulation 100000 times, find the mean, median and confidence intervals. Then we plot a histogram of the 100000 simulations.
"""

lognormval2 = np.zeros(100000) # Create an array with zereos
for i in range(100000): # For the simulation in 10,000 simulations 
    values = np.zeros(26) # Create an array with zeroes
    mu = 0.076 # Initialize mu
    sigma = 0.167 # Initialize sigma
    B_init = 50000.00 # Initialize the balance in the bank account
    deposit = 3000.00 # Initialize the deposit 
    for j in range(26): # For j in years 
        values[j] = B_init # Add the balance to the array of values
        B_init = B_init*(np.exp(np.random.normal(mu, sigma))) + deposit # Compute the new balance with lognormal distribution with the deposit 
    values = np.round(values, 2) # Round the values to two decimal places
    tab = pd.Series(values, index=pd.Index(range(40,66))) # Add to the series the new balances and indices year from 40 to 65
    lognormval2[i] = tab.iloc[-1] # Add the balance on the 65th birthday to the array of lognormal distribution values
    
## (a)

np.round(lognormval2.mean(), 2) # Find the mean of the balances on the 65th birthday

##(b)

np.round(np.median(lognormval2), 2) # Find the median of the balances on the 65th birthday


## (c)

lognormval2.sort() # Sort the balances on the 65th birthday
lognormval2[2500:97501] # Find the middle 95% values

ucl = lognormval2[2500] # Find the upper confidence limit
lcl = lognormval2[97500] # Find the lower confidence limit

print([ucl, lcl]) # Print the confidence interval

## (d)

success = lognormval2[lognormval2 > 300000.00] # Mask on the investments greater than 300000
prop = len(success) / len(lognormval2) # Find the proportion of investments greater than investment 

## (e)

plt.hist(lognormval2, bins=80, range=[0, 3500000]) # Plot the histogram


## 5. 
mu = 0.076 # Intialize mu
B_init = 50000.00 # Initilize the balance
deposit = 3000.00 # Initialize the deposit 
inflation = 0.03 # Initialize the rate of inflation
table2 = pd.DataFrame() # Create an empty data frame
for x in range(40,66): # For x in years
    year = [x] # Create a list with the years
    df = pd.DataFrame(index = year) # Rename the indices in the dataframe wit the year 
    df['Investment'] = B_init # Add the balance to the dataframe
    table2 = pd.concat([table2, df]) # Concatenate wiht the big dataframe
    B_init = B_init*(np.exp(mu)) + deposit # Compute the new balance with the deposit
    deposit = deposit*(np.exp(inflation)) # Compute the new deposit adjusted for inflation
table2 = np.round(table2, 2) # Round the values to two decimals 

"""
We now calculate the balance after 25 years while adjusting inflation each year. We repeat the simulation 100000 times.
"""" 

## 6. 
lognormval3 = np.zeros(100000) # Create an array with zeroes
inflation = 0.03 # Initialize inflation 
for i in range(100000): # For the simulation in 10,000 simulations
    values = np.zeros(26) # Create an array with zeroes 
    mu = 0.076 # Initialize mu
    sigma = 0.167 # Initialize sigma
    B_init = 50000.00 # Initialize the balance
    deposit = 3000.00 # Initialize the deposit
    for j in range(26): # For j in years
        values[j] = B_init # Add the balance to the array
        B_init = B_init*(np.exp(np.random.normal(mu, sigma))) + deposit # Compute the new balance with the deposit
        deposit = deposit*(np.exp(inflation)) # Compute the new deposit
    values = np.round(values, 2) # Round the values to two decimal places
    tab = pd.Series(values, index=pd.Index(range(40,66))) # Create a table with balances and indices as the years 
    lognormval3[i] = tab.iloc[-1] # Add the balance on the 65th birthday to the array 
    
## (a)

np.round(lognormval3.mean(), 2) # Find the mean of the balances on the 65th birthday

## (b)

np.round(np.median(lognormval3), 2) # Find the median of the balances on the 65th birthday

## (c)
lognormval3.sort() # Sort the balances
lognormval3[2500:97501] # Find the 95% middle values

ucl = lognormval3[2500] # Find the upper confidence level
lcl = lognormval3[97500]# Find the lower confidence level


print([ucl, lcl]) # Print the confidence interval

## (d)

success = lognormval3[lognormval3 > 300000.00] # Mask on investments greater than 300000
prop = len(success) / len(lognormval3) # Find the proportion of investments greater than 300000

## (e)
plt.hist(lognormval3, bins=80, range=[0, 3500000]) # Plot the histogram

"""
Now we calculate the balance of the investment after 35 years given that the investor makes a withdrawal each year.
"""

## 7. 
mu = 0.035 # Intialize mu
B_init = 616859.91 # In9tialize the balance given in 5
withdrawal = 25000.00 # Initialize the withdrawal
table3 = pd.DataFrame() # Create an empty dataframe
for x in range(65,101): #For x in years
    year = [x] # Create a list with the year
    df = pd.DataFrame(index = year) # Rename the indices of the dataframe with the year
    df['Investment'] = B_init # Add the balance to the dataframe
    table3 = pd.concat([table3, df]) # Concatenate with the big dataframe
    B_init = B_init*(np.exp(mu)) - withdrawal # Compute the balance given the withdrawal
table3 = np.round(table3, 2) # Round the values to two decimal places

"""
We simulate this calculation 100000 times, and find the mean, median, and confidence interval of these values. Then we plot a histogram of the 100000 simulations.
""" 
  
    
lognormval4 = np.zeros(100000) # Create an array with zeroes
for i in range(100000): # For the simulation in 10,000 simulations
    values = np.zeros(61) # Create an array with zeroes 
    B_init = 50000.00 # Initialize the balance
    deposit = 3000.00 # Initialize the deposit
    withdrawal = 25000.00 # Initialize the withdrawal
    inflation = 0.03 # Initialize the inflation
    for j in range(61): # For j in years 
        if j <= 25: # If in the first 25 years (year 40-65)
            mu = 0.076 # Initilize mu
            sigma = 0.167 # Initialize sigma
            values[j] = B_init # Add the balance to the dataframe
            B_init = B_init*(np.exp(np.random.normal(mu, sigma))) + deposit # Compute the new balance with the deposit
            deposit = deposit*(np.exp(inflation)) #Compute the new deposit
        else: # If in year 66-100
            mu = 0.035 # Initialize mu
            sigma = 0.051 # Initialize sigma
            values[j] = B_init # Add the balance to the dataframe
            B_init = B_init*(np.exp(np.random.normal(mu, sigma))) - withdrawal # Compute the values with withdrawal
    values = np.round(values, 2) # Round the values to two decimals
    tab = pd.Series(values, index=pd.Index(range(40,101))) # Add the values to the table
    lognormval4[i] = tab.iloc[-1] # Add the balance on the 100th birthday to the array of values
    

## (a)

np.round(lognormval4.mean(), 2) # Find the mean of the balances on the 100th birthday

## (b)

np.median(lognormval4)# Find the median of the balances on the 100thth birthday

## (c)
lognormval4.sort() # Sort the balances
lognormval3[2500:97501] # Find the middle 95% of values

ucl = lognormval4[2500] # Find the upper confidence limit
lcl = lognormval4[97500] # Find the lower confidence limit

print([ucl, lcl]) # Print the confidence interval

## (d)

success = lognormval4[lognormval4 > 0] # Mask on investments greater than 0
prop = len(success) / len(lognormval4) # Find the proportion of balances greater than 0

## (e)
plt.hist(lognormval4, bins=80, range=[-2000000, 8000000]) # Plot the histogram


    
    