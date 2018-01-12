
# coding: utf-8

# In[ ]:


def tmdbdata(id):
    import tmdbsimple as tmdb
    tmdb.API_KEY = '2dda04d609dbb288004a7fb8976646ac'
    try:
        movie = tmdb.Movies(id)
        response = movie.info()
        revenue = float(response['revenue'])
        budget = float(response['budget'])
        if revenue!=0 and budget!=0 :
            criticallist=[ROI,overview]
        else:
            criticallist=[0,0]
    except:
        print(id)
        criticallist=[id,0]
    return  criticallist

