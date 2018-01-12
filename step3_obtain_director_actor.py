#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 16:02:41 2017

@author: huaqingxie
"""

# import modules
from imdbpie import Imdb
import pandas as pd

#  to proxy requests
imdb = Imdb()
imdb = Imdb(anonymize=True) 

mydf = pd.read_csv("movie_data_filter.csv")
print mydf.head(20)

imdbid = mydf['imdbId']


director = []
actor = []
year = []
imdb_score = []
certification = []
n = 0
for line in imdbid:
    n += 1
    print "...",n
    if len(str(int(line))) == 6:
        movie = imdb.get_title_by_id("tt0" + str(int(line)))
    elif len(str(int(line))) == 5:
        movie = imdb.get_title_by_id("tt00"+str(int(line)))
    elif len(str(int(line))) == 7:
        movie = imdb.get_title_by_id("tt"+str(int(line)))
    else:
        movie = None
    if movie == None:
        director.append(" ")
        actor.append(" ")
        year.append(" ")
        imdb_score.append(" ")
        certification.append(" ")
        continue
    person_name = []
    for person in movie.directors_summary:
        person_name.append(person.name)
    str1 = ','.join(person_name)
    director.append(str1)
    actor_name = []
    for person in movie.cast_summary:
        actor_name.append(person.name)
    str2 = ','.join(actor_name)
    actor.append(str2)
    year.append(movie.year)
    imdb_score.append(movie.rating)
    certification.append(movie.certification)
mydf["year"] = year
mydf["director"] = director
mydf["actor"] = actor
mydf["imdb_score"] = imdb_score
mydf["certification"] = certification
# for every value ignore the UnicodeDecodeError
for column in mydf.columns:
    for idx in mydf[column].index:
        x = mydf.get_value(idx,column)
        try:
            x = unicode(x.encode('utf-8','ignore'),errors = 'ignore') \
            if type(x) == unicode else unicode(str(x),errors='ignore')
            mydf.set_value(idx,column,x)
        except Exception:
            mydf.set_value(idx,column,'')
            continue
        
mydf.to_csv("movie_director_actor.csv",encoding ='utf-8')
print mydf.head(20)

