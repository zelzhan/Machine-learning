#!/usr/bin/env conda
# -*- coding: utf-8 -*-
"""
* ****************************************************************************
*      Owner: stayal0ne <elzhan.zeinulla@nu.edu.kz>                          *
*      Github: https://github.com/zelzhan                                    *
*      Created: Thu May 31 15:52:11 2018 by stayal0ne                                        *
******************************************************************************
"""


# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from functools import reduce

# Importing the dataset
def import_dataset(dataset):
    dataset = pd.read_csv(dataset , sep=";")
    
    mapping1 = {"management":0, "technician" : 1, "entrepreneur":2,"admin.":3, 
               "blue-color":4, "housemaid":5, "retired":6, "self-employed":7, "services":8, 
               "student":9, "unemployed":10, "unknown": None}             #dealing with missing categorical data
    
    mapping2 = {"divorced": 0, "married":1, "single":2, "unknown":None}
    
    mapping3 = {'secondary' : 0,'primary' : 1, 'unknown' : None,'tertiary':2}
    
    mapping4 = {"success":0, "failure" : 1, "unknown": None, "other":None}     
    
    dataset['job'] = dataset['job'].map(mapping1)
    dataset['marital'] = dataset['marital'].map(mapping2)
    dataset['education'] = dataset['education'].map(mapping3)
    dataset['poutcome'] = dataset['poutcome'].map(mapping4)
    
    X = dataset.iloc[:, [i != 8 for i in range(16)]].values
    y = dataset.iloc[:, -1].values
    return X, y

def imputer(X):
    #fill in empty values
    imp = Imputer(missing_values="NaN", strategy="most_frequent", axis=0)
    imp = imp.fit(X[:, [1, 2, 3, -1]])
    X[:, [1, 2, 3, -1]] = imp.transform(X[:, [1, 2, 3, -1]])
    return X

def encoder(X, y):
    #label encoding
    label_encoder_X = LabelEncoder()
    X[:, 4] = label_encoder_X.fit_transform(X[:, 4])     
    X[:, 6] = label_encoder_X.fit_transform(X[:, 6])    
    X[:, 7] = label_encoder_X.fit_transform(X[:, 7])         
    X[:, 9] = label_encoder_X.fit_transform(X[:, 9])     
    one_hot_encoder = OneHotEncoder(categorical_features=[1, 2, 3, 9, -1])   #create an OneHotEncoder object specifying the column
    X = one_hot_encoder.fit_transform(X).toarray()              #OneHot encode
    label_encoder_y = LabelEncoder()                            #same operations for the values which we want to predict
    y = label_encoder_y.fit_transform(y)
    return X, y

def split(X, y):
    # Splitting the dataset into the Training set and Test set
    from sklearn.cross_validation import train_test_split
    return train_test_split(X, y, test_size = 0.25)

def scale(X_train, X_test):
    # Feature Scaling
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    return X_train, X_test

def train(X_train, y_train):
    # Fitting Kernel SVM to the Training set
    from sklearn.svm import SVC
    classifier = SVC(kernel = 'rbf')
    classifier.fit(X_train, y_train)
    return classifier

def conf_matrix():
    # Making the Confusion Matrix
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)
    
def preprocessing(dataset):
    X, y = import_dataset(dataset)
    X = imputer(X)
    X, y = encoder(X, y)
    X_train, X_test, y_train, y_test = split(X, y)
    X_train, X_test = scale(X_train, X_test)
    return X_train, X_test, y_train, y_test

def grid_search(classifier, X_train, y_train):
    from sklearn.model_selection import GridSearchCV
    params = [{'C':[1, 5, 10], 'kernel':['linear']}]
    grid = GridSearchCV(estimator = classifier,
                        param_grid = params,
                        scoring = 'accuracy',
                        cv = 10,
                        n_jobs = -1)
    grid = grid.fit(X_train, y_train)
    return grid
    
if __name__ == '__main__':
    dataset = "bank-full.csv"
    X_train, X_test, y_train, y_test = preprocessing(dataset)
    classifier = train(X_train, y_train)
    y_pred = classifier.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    grid_object = grid_search(classifier, X_train, y_train)
    
#    k_fold_accuracy = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10, n_jobs=-1)
#    k_fold_accuracy.mean()

# linear = 0.8955144
# polynomial = 0.89719
# sigmoid = 0.86516
# rbf = 0.900371

