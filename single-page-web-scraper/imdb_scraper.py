import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

import numpy as np

url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
headers = {"Accept-Language": "en-US, en;q=0.5"}
results = requests.get(url, headers=headers)


#specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
soup = BeautifulSoup(results.text, "html.parser")
#printing soup in a more structured tree format that makes for easier reading

titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

movie_div = soup.find_all('div', class_='lister-item mode-advanced')

for container in movie_div:

        #Name
        name = container.h3.a.text
        titles.append(name)
        
        #Year
        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)

        # runtime
        # runtime = container.p.find('span', class_='runtime').text
        # time.append(runtime)
        runtime = container.p.find('span', class_='runtime').text if container.p.find('span', class_='runtime').text else '-'
        time.append(runtime)

        #IMDB rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        # # #Metascore
        m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        metascores.append(m_score)

        #There are two NV containers, grab both of them as they hold both the votes and the grosses
        nv = container.find_all('span', attrs={'name': 'nv'})
        
        #filter nv for Votes
        vote = nv[0].text
        votes.append(vote)
        
        #filter nv for grosses
        grosses = nv[1].text if len(nv) > 1 else '-'
        us_gross.append(grosses)


# print(titles)
# print(years)
# print(time)
# print(imdb_ratings)
# print(metascores)
# print(votes)
# print(us_gross)

movies = pd.DataFrame({
'movie': titles,
'year': years,
'timeMin': time,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes,
'us_grossMillions': us_gross,
})


## CLEANING DATA IN PANDAS##'
# remove the commas from the votes data
# movies['votes'] = movies['votes'].str.replace(',', '').astype(int)

# remove the parenthesis and only grab the ints from the year data
# movies.loc[:, 'year'] = movies['year'].str[-5:-1].astype(int)



# # remove the $ and M from the gross data
# movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))

# # remove the 'min' from the timeMin data
# movies['timeMin'] = movies['timeMin'].astype(str)
# movies['timeMin'] = movies['timeMin'].replace(np.nan, '', regex=True)
# movies['imdb'] = movies['imdb'].astype(float)
# # there was lots of white space and brackets. this will turn data back to string
# # movies['metascore'] = movies['metascore'].astype(str)
# # #this will grab only integers
# movies['metascore'] = movies['metascore'].str.extract('(\d+)')

# # #this will turn any NaN in metascore to a blank space 
# # movies['metascore'] = movies['metascore'].replace(np.nan, '', regex=True)


movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['metascore'] = movies['metascore'].astype(int)
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)




movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))

movies['us_grossMillions'] = pd.to_numeric(movies['us_grossMillions'], errors='coerce')



# print(movies)
# print(movies.dtypes)


# print(movies.isnull().sum())
movies.to_csv('movies.csv')


# movies['us_grossMillions'] = movies['us_grossMillions'].replace(np.nan, '-', regex=True)

# .astype('Int64')

# ].replace(np.nan, '-', regex=True)


# movies.to_csv('movies.csv')

# # Making a list of missing value types
# missing_values = [" ", "-", "NaN"]
# movies = pd.read_csv("movies.csv", na_values = missing_values)

# print(movies['us_grossMillions'])
# print(movies['us_grossMillions'].isnull())