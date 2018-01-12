
# coding: utf-8

# In[3]:


#install graphlab create
import graphlab as gl
movies = gl.SFrame.read_csv("new_movies_creidt_top.csv",column_type_hints=[long,long,long,list,str,str,float,str,str,str,long,long,long,str,str,list,long,str,str,long,str,str,float,str,long,long])


# In[ ]:


#chart
movies['genres_y'].show()
movies['popularity'].show()
movies.show()
#construct ROI
ROI=gl.SArray(movies['revenue']/movies['budget'])
movies.add_column(ROI, name='ROI')
movies['ROI'].show()
#model selection
data =  movies
# ROIwith rating >=3 are good
data['is_good'] = data['ROI'] >= 3
data=data.dropna()
# Make a train-test split
train_data, test_data = data.random_split(0.8)

# Automatically picks the right model based on your data.
model = gl.classifier.create(train_data, target='is_good',
                             features = ['popularity','budget','vote_average','vote_count'])

# Generate predictions (class/probabilities etc.), contained in an SFrame.
predictions = model.classify(test_data)


# In[ ]:


#model performance
# Make a train-test split
train_data, test_data = data.random_split(0.8)
btmodel = gl.boosted_trees_classifier.create(train_data, target='is_good',features = ['popularity','budget','imdb_score','vote_average','vote_count','director_credit','actor_credit'],
                                           max_iterations=10,
                                           max_depth = 3)
lgmodel = gl.logistic_classifier.create(train_data, target='is_good',
                                   features = ['popularity','budget','imdb_score','vote_average','vote_count','director_credit','actor_credit'])
# Save predictions to an SFrame (class and corresponding class-probabilities)
btpredictions = btmodel.classify(test_data)
lgpredictions = lgmodel.classify(test_data)
# Evaluate the model and save the results into a dictionary
btresults = btmodel.evaluate(test_data)
lgresults = lgmodel.evaluate(test_data)

