#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 16:50:20 2018

@author: colleencallahan
"""

import os
os.chdir('/Users/colleencallahan/Desktop')
print(os.getcwd())


""" The following code reads in the movie review datasets, 'reviews', 'genres', and 'reviewers' as csv files.
"""

import pandas as pd # Load pandas as pd
import numpy as np # Load NumPy as np
reviews = pd.read_csv('reviews.txt', 
                        sep='\t',
                        header=None,
                        names=['Reviewer','Movie','Rating','Date']) # Read in reviews.txt

movies = pd.read_csv('genres.txt', sep='|', header=None, names=['movie id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure', 'Animation',
	'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
	'FilmNoir', 'Horror', 'Musical', 'Mystery', 'Romance', 'SciFi',
	'Thriller', 'War', 'Western']) # Read in genres.txt
del movies['IMDb URL']
del movies['video release date']

reviewers = pd.read_csv('reviewers.txt', sep='|', header=None, names=["Reviewer", "Age", "Gender", "Occupation", "Zip Code"]) # Read in reviewers.txt



"""
The following code explores the movie review datasets. 

Here we find the average rating from the top 5 movie reviewers with a confidence interval.
We then find the average rating from all reviews that are not from top 5 reviewers
"""

top_reviewers = reviews['Reviewer'].value_counts()[0:5].index # Extract the reviewer IDs for the 5 revievers that gave the most reviews
reviewer = reviews['Reviewer'].isin(top_reviewers) # Return True for the column 'Reviewer' if the review was from a top 5 reviewer, False if form a different reviewer 
reviewer_index = reviewer[reviewer == True].index # Return the index  of the reviews that came from top 5 reviewers
ratings = reviews['Rating'][reviewer_index] # Find the ratings from all the top 5 reviewers
n = ratings.count() # Count the number of ratings from top 5 reviewers
avg_rating = ratings.mean() # Find the average rating from the top 5 reviewrs

s = np.std(ratings, ddof = 1) # Find standard deviation from top 5 reviewers
moe = 1.96*(s/((n)**(1/2))) # Find the margin of error 
lcl = avg_rating - moe # Find the lower confidence limit
ucl = avg_rating + moe # Find the upper confidence limit 
print([lcl,ucl]) # Print confidence interval 


other_reviewer = ~reviews['Reviewer'].isin(top_reviewers) # Return True for the column 'Reviewer' if the review was from a reviewer other than the top 5 reviewers, False if from the top 5 reviewers
other_reviewer_index = other_reviewer[other_reviewer == True].index # Return index of all the other reviewers
avg_ratings_other = reviews['Rating'][other_reviewer_index].mean() # Find the mean rating of all the reviews that are not from the top 5 reviewers



"""
Here we find the top 10 movies with the most reviews 
"""

num_reviewed = reviews['Movie'].value_counts()[0:10] # Extract the movies with the most reviews 
num_reviewed = pd.DataFrame(num_reviewed) # Convert to dataFrame
num_reviewed = num_reviewed.sort_index() # Sort by index


top_10_movies = reviews['Movie'].value_counts()[0:10].index # Find the top 10 movies with the most amount of reviews and extract the movie id

topmovies = movies[movies['movie id'].isin(top_10_movies) == True] # Find the top 10 movies in the list of movies

topmovieid = topmovies.loc[:,'movie id':'movie title'] # Extract columns movie id and movie title from the top 10 movies

topmovieid['Number of Reviews'] = num_reviewed['Movie'].values # Add column with number of reviews for each movie to the dataFrame topmovieid

"""
Here we find most reviewed genre
"""

movie_genre = movies.loc[:,'Action':].sum() # Sum the number of reviews from each genre 


movie_genre[movie_genre == movie_genre.max()] # Find the max number of reviews and which genre is associated with the most number of reviews 


"""
Here we find the percent of movies that are classified as having more than one genre
"""
genre = movies.loc[:,'Action':].sum(axis=1) # Sum the genres on rows (for each review)

greater_than_one = genre[genre > 1].count() # Count the number of reviews that had more than one genre (sum was greater than one)

percentage = (greater_than_one / genre.count()) * 100 # Find the percentage of reviews that are classified as more than one genre


"""
Next, we split the data by gender of reviewer. We then find the averages with confidence intervals of male and female reviewers.
"""

review_gender = reviewers['Reviewer'].groupby(reviewers['Gender']) # Group Reviewer by gender

male = reviewers[reviewers['Gender'] == 'M'] # Extract reviews from Males
female = reviewers[reviewers['Gender'] == 'F'] # Extract reviews from females

male_userid = male['Reviewer'] # Extract the reviewer IDs from male reviews
female_userid = female['Reviewer'] # Extract the reviewer IDs from female reviews

male_ratings = reviews[reviews['Reviewer'].isin(male_userid) == True]['Rating'] # Extract the ratings from the male reviewers
female_ratings = reviews[reviews['Reviewer'].isin(female_userid) == True]['Rating'] # Extract the ratings from the female reviewers

s1 = np.std(male_ratings, ddof = 1) # Find standard deviation of male ratings
s2 = np.std(female_ratings, ddof = 1) # Find standard deviation of female ratings
x1 = male_ratings.mean() # Average of male ratings
x2 = female_ratings.mean() # Average female ratings
n1 = male_ratings.count() # Number of male ratings
n2 = female_ratings.count() # Number of female ratings

moe1 = 1.96*(s1/(n1**(1/2))) # Find the margin of error for males
moe2 = 1.96*(s2/(n2**(1/2))) # Find the margin of error for females 

ci_male = (x1 - moe1, x1 + moe2) # Compute confidence interval for males
ci_female = (x2 - moe2, x2 + moe2) # Compute confidence interval for female

"""
Here write a function that converts the zipcodes in the data set to state using regular expression. We then add the column "State" to the dataframe. We then find the top 10 territoties with the most reviews.
"""

import re # Import regular expression
def ziptostate(zcode): # Define a function ziptostate that takes one argument zcode
    if re.search('[a-zA-Z]+', zcode): # If zipcode contains a letter 
        return('Canada') # Return Canada
    elif zcode in zipseries.index: # If it does not contain a letter
        return(zipseries[zcode]) # Convert to state
    else:
        return('Unknown') # Otherwise return unknown
states = reviewers['Zip Code'].apply(ziptostate) # Apply zip to state to all zipcodes
reviewers['State'] = states # Add a new column in reviewers with the states for each review


reviewers.columns = ["Reviewer", "Age", "Gender", "Occupation", "Zip Code", "State"] # Rename columns in reviewers

newdf = pd.merge(reviews, reviewers) # Merge dataFrames reviews and reviewers on "Reviewer"

location_num_reviews = newdf['State'].value_counts() # Count the number of reviews from each territory

location_num_reviews[0:10] # Find the top 10 territories with the most reviews


"""
Here we explore the occupations of the reviewers and find the occupation of the reviewer with the highest average rating.
"""


newdf = pd.merge(reviews, reviewers) # Merge two dataFrames reviews and reviewers on "Reviewer"
avg_occupation = newdf['Rating'].groupby(newdf['Occupation']).mean() # Group ratings by occupation and find the average rating for each occupation
avg_occupation = avg_occupation.drop(avg_occupation.index[[12,13]]) # Delete 'other' and 'none' from the occupation list

avg_occupation[avg_occupation == avg_occupation.max()] # Find the occupation with the highest review


"""
Next we find the percent of movies that had 1 through 20 reviews
"""

movierev = reviews['Movie'].value_counts(ascending=True) # Find all the counts for the number of times each movie was reviewd
percentage = movierev.value_counts() / movierev.count() * 100 # Find the percentage of movies that had 1,2,... etc. reviews

percentage.sort_index()[0:20] # Find the percentage of movies that had exactly 1 through 20 reviews


"""
Here we find the genres with the highest and lowest ratings.
"""

movies = movies.rename(columns={'movie id' : 'Movie'}) # Rename column movie id as Movie

mergedf = pd.merge(movies, newdf) # Merge dataFrame movies with dataFrame new df on "Movie"

genres = ['Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy','FilmNoir', 'Horror', 'Musical', 'Mystery', 'Romance', 'SciFi','Thriller', 'War', 'Western'] # Create a list of all the genres

max_rating = 0 # Initialize max rating
for genre in genres: # Iterate through genres
    rating = mergedf[mergedf[genre] == 1]['Rating'].mean()  # Find the average rating for each genre
    if rating > max_rating: # If this rating is greater than the max rating
        max_rating = rating # Set a new max rating
        max_genre = genre # This genre is the new max genre
print(max_genre) 

min_rating = 100 # Initialize min rating
for genre in genres:  # Iterate through genres
    rating = mergedf[mergedf[genre] == 1]['Rating'].mean() # Find the average rating for each genre
    if rating < min_rating: # If this rating is less than the min rating
        min_rating = rating# Set a new min rating
        min_genre = genre # This genre is the new min genre
print(min_genre) 


"""
Here we find the porportions of positive male and female ratings; "postiv"e being defined as ratings greater than 4. Then we find the confidence intervals for the proportions.
"""

posmale = male_ratings[male_ratings >= 4] # Extract all the male ratings greater than 4

posfemale = female_ratings[female_ratings >=4] # Extract all female ratings greater than 4 

pm = posmale.count() / male_ratings.count() # Find the proportion ofpositive male ratings
pf = posfemale.count() / female_ratings.count() # Find the proportion of positive female ratings
n1 = male_ratings.count() # Number of male ratings
n2 = female_ratings.count() # Number of female ratings


moe = 1.96*(pf*(1-pf)/n1 + pm*(1-pm)/n2)**0.5 # Margin of error for difference in proportions
lcl = (pf-pm) - moe  # Lower confidence limit
ucl = (pf-pm) + moe  # Upper confidence limit
print([lcl,ucl])  # Print the confidence interval

"""
Last, we find the proportions of positive reviews from Canada and the U.S., as well as the confidence intervals for the proportions.
"""

Canada_reviews = newdf[newdf['State'] == 'Canada'] # Extract all the reviews from Canada
US_reviews = newdf[newdf['State'] != ('Canada' or 'Unknown')] # Extract all the reviews from US territories

posC = Canada_reviews[Canada_reviews['Rating'] >= 4]['Rating'] # Extract positive reviews from Canada
posU = US_reviews[US_reviews['Rating'] >= 4]['Rating'] # Extract positive reviews from US territories

pC = posC.count() / Canada_reviews['Rating'].count() # Proportion of positive Canadian reviews
pA = posU.count() / US_reviews['Rating'].count() # Proprotion of positive US reviews
n1 = Canada_reviews['Rating'].count() # Number of Canadian reviews
n2 = US_reviews['Rating'].count() # Number of US reviews


moe = 1.96*(pC*(1-pC)/n1 + pA*(1-pA)/n2)**0.5 # Margin of error for difference in proportions 
lcl = (pC-pA) - moe  # Lower confidence limit
ucl = (pC-pA) + moe  # Upper confidence limit
print([lcl,ucl]) # Print confidence interval


