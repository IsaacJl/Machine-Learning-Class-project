#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 01:34:40 2017

@author: huaqingxie
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
mydf = pd.read_csv("movie_director_actor.csv")


director = mydf["director"]
actor = mydf["actor"]

director_credit = []
actor_credit = []
print len(director)
print len(actor)

n = 0
for line in director:
    n += 1
    print n
    n1 = 0.
    for name in line.split(','):
        name = name
        page_url = "https://www.themoviedb.org/search?query=" + name
        page = requests.get(page_url)
        if page.status_code != 200: # a status code !=200 indicates a failure
            page_url = None        # exit the loop
        else:                       # status_code 200 indicates success
            soup = BeautifulSoup(page.content, 'html.parser')
            hrefs = soup.select("a[href^=/person/]")
            links = [link.attrs.get('href') for link in hrefs]
            if links != []:
                page_url = "https://www.themoviedb.org" + links[0]
            else:
                n1 += 0
                continue
            # print page_url
            page = requests.get(page_url)
            if page.status_code != 200: # a status code !=200 indicates a failure
                page_url = None        # exit the loop
            else:                       # status_code 200 indicates success
                soup = BeautifulSoup(page.content, 'html.parser')
                divs = soup.select("div#left_column p")
                text = divs[1].get_text()
                for s in text.split():
                    if s.isdigit():
                        credit = int(s) 
                n1 += credit
    director_credit.append(n1)

n = 0
for line in actor:
    n += 1
    print n
    n2 = 0.
    for name in line.split(','):
        name = name
        page_url = "https://www.themoviedb.org/search?query=" + name
        page = requests.get(page_url)
        if page.status_code != 200: # a status code !=200 indicates a failure
            page_url = None        # exit the loop
        else:                       # status_code 200 indicates success
            soup = BeautifulSoup(page.content, 'html.parser')
            hrefs = soup.select("a[href^=/person/]")
            links = [link.attrs.get('href') for link in hrefs]
            if links != []:
                page_url = "https://www.themoviedb.org" + links[0]
            else:
                n2 += 0
                continue
            # print page_url
            page = requests.get(page_url)
            if page.status_code != 200: # a status code !=200 indicates a failure
                page_url = None        # exit the loop
            else:                       # status_code 200 indicates success
                soup = BeautifulSoup(page.content, 'html.parser')
                divs = soup.select("div#left_column p")
                text = divs[1].get_text()
                for s in text.split():
                    if s.isdigit():
                        credit = int(s) 
                n2 += credit
    actor_credit.append(n2)

print "~~~~~~" 
mydf["director_credit"] = director_credit
print "..."
mydf["actor_credit"] = actor_credit
print '++++++'   
mydf.to_csv("movies_known_credit.csv")


                