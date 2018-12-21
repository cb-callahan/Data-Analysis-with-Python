"""
Created on Wed Dec 19 17:21:43 2018

@author: colleencallahan
"""

"""
Here we read in the dataset for pizza requests from Reddit.
"""
import pandas as pd # Load pandas as pd
import numpy as np # Load numpy as np

lines =  pd.Series(open('pizza_requests.txt').read().splitlines())



"""
We find the proportion of requests that are successful
"""

x = lines[lines.str.contains('requester_received_pizza')].str.split(' ').str[1]
# Mask over the lines that contain "requester_received_pizza" and isolate 
# whether the 'true' or 'false' indicating whether or not the requester 
# received a pizza

true = x[x.str.contains('true')].count() # Isolate the lines for which 
# "requester_received_pizza" was true and count the number of these 

proportion = true / x.count() # Find the proportion of requests that were 
# "true" i.e successful

"""
(1)
proportion = 0.24634103332745547
"""

"""
Next, we find the median age in days of the requester accounts at the time of the request.
"""

x = lines[lines.str.contains("requester_account_age_in_days_at_request")].str.split(' ').str[1]
# Mask over the lines that contain "requester_account_age_in_days_at_request" 
# and isolate the value of the account age  

x.median() # Find the median of these values 


"""
(2)
155.6475925925926
"""

"""
Here we find the proportion of successful pizza requests for older accounts and for newer accounts, and then find the confidence interval for the difference between older and newer accounts.
"""

x = lines[lines.str.contains("requester_account_age_in_days_at_request")].str.split(' ').str[1]
# Isolate the age from the lines that contain "requester_account_age_in_days_at_request" 

x = pd.DataFrame(x) # Convert the Series into a Data Frame
x.columns = ['values'] # Name the column that contains the ages 'values'
x['values'] = x['values'].astype(float) # Convert these values from string 
# to float

n1 = x[x['values'] > 155.6475925925926].count() # Count the number of ages 
# above the median as the number of old accounts
n2 = x[x['values'] <= 155.6475925925926].count() # Count the number of ages 
# above the median as newer accounts

lines2 = pd.Series(open('pizza_requests.txt').read().split('%%%%%%%%%%')) # Split on each request
lines3 = lines2[lines2.str.contains('"requester_received_pizza", true')] # Find all the lines for which the pizza request is true
lines4 = lines3[lines3.str.contains("requester_account_age_in_days_at_request")].str.split('\n').str[11] # Isolate the lines with the account age for the requests that were successful

lines5 = lines4.str.split(',').str[1] # Isolate the age of the account from 
# the line with "requester_account_age_in_days_at_request"
lines5 = lines5.astype(float) # Convert all the values to float

lines5 = pd.DataFrame(lines5) # Convert the series with all the ages of the 
# various accounts into a Data Frame
lines5.columns = ['values'] # Name the column of ages "values"

older_accounts = lines5[lines5['values'] > 155.6475925925926].count() # Count
# the number of accounts that had successful pizza requests and ages above 
# the median age 
newer_accounts = lines5[lines5['values'] <= 155.6475925925926].count()# Count
# the number of accounts that had successful pizza requests and ages below or  
# equal to the median age


phat1 = older_accounts / n1 # Find the proportion of successful requests 
# among older accounts 
phat2 = newer_accounts / n2 # Find the proportion of successful requests 
# among newer accounts 

ci = ((phat1 - phat2) - 1.96*(((phat1*(1-phat1))/n1) + ((phat2*(1-phat2))/n2))**(1/2), (phat1 - phat2) + 1.96*(((phat1*(1-phat1))/n1) + ((phat2*(1-phat2))/n2) )**(1/2)) # Find the 
# confidence interval for difference in proportion of successful pizza requests 
# between the older accounts and newer accounts

""""
(3)
(0.022477,0.067275)
"""

"""
Here we find the percentage of successful requests for students and children.
"""

request = lines[lines.str.contains("request_text")].str.split('"').str[3].str.lower()
# Isolate the text of the request and convert the entire text lowercase letters

student = request[request.str.contains('student')].count() # Count the number
# of requests that mention student
children = request[request.str.contains('children')].count() # Count the number
# of requests that mention children


request_student = request[request.str.contains('student')] # Isolate the lines
# that contain the word student 
student_and_children = request_student[request_student.str.contains('children')].count()
# Of the lines that contain student, count the lines that also contain the 
# word children


total = student + children - student_and_children # Add the number of lines
# that contain 'children' and the number of lines that contain 'student'
# and substract the number of lines that contain both 'children' and 'student'
# so that those lines are not counted twice

total_requests = lines[lines.str.contains('requester_received_pizza')].count()
prop = total / total_requests * 100

"""
(4) 
18.003879386351613 %
"""

"""
Next, we find the number of requests from Canada.
"""

line = lines[lines.str.contains("request_title")].str.lower() # Isolate all the 
# lines that contain "request_title" and convert all letters to lowercase

Canada = line[line.str.contains('canada')].count() # Isolate all the lines
# that contain Canada and count the number of lines

"""
(5)
103
"""

"""
Now, we find the proportion and confidence interval of pizza requests donated anonymously.
"""

lines2 = pd.Series(open('pizza_requests.txt').read().split('%%%%%%%%%%')) # Split on each request
lines3 = lines2[lines2.str.contains('"requester_received_pizza", true')] # Find all the lines for which the pizza request is true
total_success = lines3.count() # Find the total number of successful requests
request = lines3[lines3.str.contains("giver_username_if_known")].str.split('\n').str[1]
# Isolate the line with "giver_username_if_known"
request_anon = request[request.str.contains('N/A')].count() # Count the number
# of times "giver_username_if_known" has "N/A", or an anonymous giver

p_hat = request_anon / total_success # Find the proportion of anonymous 
# givers over the succesful requests

n = total_success # The total number of successful requests

ci = (p_hat - 1.96 * (p_hat * (1-p_hat)/n)**(1/2),
                     p_hat + 1.96 * (p_hat * (1-p_hat)/n)**(1/2)) # Find a 
      # 95% confidence interval for the proportion of successful pizza 
      # requests donated anonymously

"""
(6)
(0.68923367864998963, 0.73667899135716863)
"""

"""
We find the maximum number of subreddits.
"""

number_subreddit = lines[lines.str.contains("requester_number_of_subreddits_at_request")].str.split(' ').str[1] # Find the lines that contain "requester_number_of_subreddits_at_request"
# and isolate the number of subreddits

number_subreddit.max() # Find the maximum number of subreddits

print(number_subreddit.astype(int).max())

"""
(7)
99
"""


"""
We find the top 10 subreddits and write these subreddits to a txt file. 
""" 

subreddit = lines.index[lines.str.strip().str.split().str.len() == 1] # Strip
# each line of spaces, split each line on spaces and then isolate all the lines
# of length one
x = lines.index[lines.str.contains("%%%%%%%%%%")] # Isolate all the lines that 
# contain "%%%%%%%%%%"
y = lines.index[lines.str.contains('}')] # Isolate all lines that contain '}'

x1= subreddit.difference(x) # Find the lines of length one that are not 
# "%%%%%%%%%%"
x2 = x1.difference(y) # Find all the lines of length one that are not 
# "%%%%%%%%%%" or "}"

subreddits = lines[x2] # Isolate all subreddits by finding the lines that have
# the index of lines that are length one and not "%%%%%%%%%%" or "}"
top_subreddits = subreddits.value_counts() # Find the value counts for each
# subreddit
top10 = top_subreddits[:10] # Find the top 10 subreddits

fh = open('cc5dh-assignment07-subreddits.txt', 'w') # Open a new file to write

for i in range(len(top10)): # For each top 10 subreddit
    fh.write(top10.index[i]) # Write the subreddit to the file
    fh.write(', ')
    fh.write(str(top10[i])) # Write the count of the subreddit to the file
    fh.write("\n")
    

fh.close() # Close the file

"""
(8)
  "AskReddit"                3216
  "funny"                    2655
  "pics"                     2610
  "IAmA"                     2128
  "WTF"                      2121
  "gaming"                   2058
  "Random_Acts_Of_Pizza"     1597
  "AdviceAnimals"            1450
  "todayilearned"            1368
  "aww"                      1295
  """
  


