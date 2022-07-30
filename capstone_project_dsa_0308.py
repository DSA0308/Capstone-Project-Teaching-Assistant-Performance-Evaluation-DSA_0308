# -*- coding: utf-8 -*-
"""Copy of Capstone Project - DSA_0308.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MK7uU4-6TqWq3fp3floETYCtTfXSVJXP

### **Machine Learning Foundations**

Capstone Project - Teaching Assistant Performance Evaluation

Registration Number - DSA_0308
"""

import numpy as np
import pandas as pd

from matplotlib import pyplot
import seaborn as sns

import numpy as np
import pandas as pd

# Data visualization
import matplotlib.pyplot as plt
from matplotlib import cm # Colomaps
import seaborn as sns

# Classifier algorithms
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

#train test split
from sklearn.model_selection import train_test_split

# Model evaluation
from sklearn import metrics

"""Load Data"""

file_name = 'https://archive.ics.uci.edu/ml/machine-learning-databases/tae/tae.data'

data = pd.read_csv(file_name, header=None)
data.head()

"""Pre-process Data for Training"""

data.columns = ['English Speaking', 
                'Course instructor',
                'Course',
                'Semester',
                'Class size',
                'Performance']

data.describe(include='all').transpose()

data.info()

data['id'] = data.index+1
data

data.columns

data['Performance'].value_counts()

correlation_matrix = data[['English Speaking','Course instructor','Course','Semester','Class size','Performance']].corr()

sns.heatmap(correlation_matrix)
correlation_matrix

X_variables = ['English Speaking','Course instructor','Course','Semester','Class size']
data[X_variables].head()

y_varibale = 'Performance'
data[y_varibale].head()

X = data[X_variables].values
X

y = data[y_varibale].values
y

"""Data Pre-processing"""

def pre_processing(data):    
    data['id'] = data.index+1

    X_variables = ['English Speaking','Course instructor','Course','Semester','Class size']
    
    for x in list(set(X_variables) - set(data.columns)):
        data[x] = 0
        
    return data[X_variables]

"""Train Test Split"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(F"Train sample size = {len(X_train)}")
print(F"Test sample size  = {len(X_test)}")

"""Model Training Function"""

def model_train(model, model_name, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_pred_prob = model.predict_proba(X_test)[:, 1]
    test_result = pd.DataFrame(data={'y_act':y_test, 'y_pred':y_pred, 'y_pred_prob':y_pred_prob})

    accuracy = metrics.accuracy_score(test_result['y_act'], test_result['y_pred']) 
    precision = metrics.precision_score(test_result['y_act'], test_result['y_pred'], average='weighted', pos_label=1)
    f1_score = metrics.f1_score(test_result['y_act'], test_result['y_pred'], average='weighted') 
  
    return ({'model_name':model_name, 
                   'model':model, 
                   'accuracy':accuracy, 
                   'precision':precision,
                  'f1_score':f1_score,
                  })

model0 = model_train(RandomForestClassifier(n_estimators=500, max_depth=10, n_jobs=3, verbose=1), 'rf_new', X_train, y_train, X_test, y_test)

model0

models = []
models.append(model_train(LogisticRegression(n_jobs=3, verbose=1), 'lgr1', X_train, y_train, X_test, y_test))
models.append(model_train(RandomForestClassifier(n_estimators=100, max_depth=None, n_jobs=3, verbose=1), 'rf1', X_train, y_train, X_test, y_test))
models.append(model_train(RandomForestClassifier(n_estimators=500, max_depth=None, n_jobs=3, verbose=1), 'rf2', X_train, y_train, X_test, y_test))
models.append(model_train(RandomForestClassifier(n_estimators=500, max_depth=10, n_jobs=3, verbose=1), 'rf3', X_train, y_train, X_test, y_test))
models.append(model_train(RandomForestClassifier(n_estimators=500, max_depth=20, n_jobs=3, verbose=1), 'rf4', X_train, y_train, X_test, y_test))
models = pd.DataFrame(models)
models

from sklearn.model_selection import GridSearchCV

parameters = {'n_estimators': [100,500], 'max_depth': [None, 10, 20]}
gs_model = GridSearchCV(RandomForestClassifier(), parameters, n_jobs=2, verbose=3, pre_dispatch=2)
gs_model.fit(X_train, y_train)

print(gs_model.best_params_)

from sklearn.metrics import classification_report, confusion_matrix 

y_pred = gs_model.predict(X_test) 

print(classification_report(y_test, y_pred)) 
print(confusion_matrix(y_test, y_pred))

model = models.query("model_name=='rf2'")
model

model = model['model'].values[0]
model

"""Saving Best Model"""

import pickle

save_file = 'model_rf2_test.pickle'
pickle.dump(model, open(save_file, 'wb'))

model_ = pickle.load(open(save_file, 'rb'))
model_

import joblib

save_file = 'model_rf2_test.joblib'
joblib.dump(model, open(save_file, 'wb'))

model_ = joblib.load(save_file)
model_

"""Predict on a Sample Data"""

sample_input = data[['English Speaking','Course instructor','Course','Semester','Class size']].sample(10)
sample_input

pre_processing(sample_input)

model.predict_proba(pre_processing(sample_input))

"""Score Function"""

def score(input_data, model):
    return model.predict_proba(input_data)

prediction = score(input_data=pre_processing(sample_input), model=model)
prediction

"""Post-processing"""

def post_processing(prediction):
    if len(prediction)==1:
        return prediction[:, 1][0]
    else:
        return prediction[:, 1]

output = post_processing(score(input_data=pre_processing(sample_input), model=model))
output

sample_input['prediction'] = post_processing(model.predict_proba(pre_processing(sample_input)))
sample_input

sample_output = post_processing(score(input_data=pre_processing(sample_input), model=model))
sample_output

"""Inference Pipeline"""

def app_prediction_function(input_data, model):
    return post_processing(score(input_data=pre_processing(input_data), model=model))

input_data = data[['English Speaking','Course instructor','Course','Semester','Class size']].sample(1)
print(input_data)
app_prediction_function(input_data, model)

input_data = input_data.to_dict(orient='records')[0]
input_data

input_data = pd.DataFrame([input_data])
input_data

"""Get Prediction"""

app_prediction_function(input_data, model)