#!/usr/bin/python

"""
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:
    Sara has label 0
    Chris has label 1
"""

import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess
from sklearn import svm
from sklearn.metrics import accuracy_score
import datetime
import pandas as pd

### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()


clf = svm.SVC(C=10000.0, kernel='rbf')

#features_train = features_train[:len(features_train)/100]
#labels_train = labels_train[:len(labels_train)/100]

print("fitting")
print(datetime.datetime.now())
clf.fit( features_train, labels_train)
print(datetime.datetime.now())

print("predicting")
print(datetime.datetime.now())
pred = clf.predict(features_test)
print(datetime.datetime.now())

print("scoring")
print(datetime.datetime.now())
print(accuracy_score(pred, labels_test))
print(datetime.datetime.now())

count = 0

for p in pred:
    if p == 1:
        count = count + 1

print(count)


analysis = pd.DataFrame(pred)
print(analysis.head(100))
chris = analysis[analysis[0] == 1]
print(chris.head(100))
print(chris.count())
