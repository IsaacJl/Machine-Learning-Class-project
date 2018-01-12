#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 16:49:13 2017

@author: huaqingxie
"""
# import modules
import csv
from imdbpie import Imdb
import pandas as pd

#  to proxy requests
imdb = Imdb()
imdb = Imdb(anonymize=True) 

# open the csv file to find the movie id
with open('movies_list.csv', 'r') as f:
    reader = csv.reader(f, delimiter=",")
    n = 0
    mydf = {}
    for line in reader:
        # indicate if it is still working 
        print "..."
        # skip the first line
        if n == 0:
            n += 1
            continue
        else:
            imdbid = line[1]
            tmdbid = line[2]
            title = line[3]
            genres = line[4]
            # get teh reviews region based on length of imdbid
            if len(imdbid) == 6:
                reviews = imdb.get_title_reviews("tt0"+imdbid)
            elif len(imdbid) == 5:
                reviews = imdb.get_title_reviews("tt00"+imdbid)
            elif len(imdbid) == 7:
                reviews = imdb.get_title_reviews("tt"+imdbid)
            list_ = []
            if reviews == None:
                list_ = []
            else:
                for line in reviews:
                    # delete the data cannot encode by 'utf-8'
                    try: 
                        line.text.encode('utf-8')
                    except UnicodeEncodeError:
                        continue
                    except AttributeError:
                        continue
                    
                    try: 
                        line.summary.encode('utf-8')
                    except UnicodeEncodeError:
                        continue
                    except AttributeError:
                        line = line
                    # get the data
                    list_.append((line.text,line.date,line.rating,\
                                  line.summary,line.status,line.user_location,\
                                  line.user_score,line.user_score_count))
                # convert to data frame
                df = pd.DataFrame(list_)
                # set the dictionary
                mydf[imdbid,tmdbid,title,genres] = df

# concat the data frame
mydf = pd.concat(mydf)

# change index to columns
mydf = mydf.reset_index(level=[0,1,2,3,4])

# set index
mydf.index = range(len(mydf))

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
        
# save to csv file
mydf.to_csv('movie_data_review.csv',encoding ='utf-8') 

# the dataset is huge, the movie_data.csv in zip is a subset

