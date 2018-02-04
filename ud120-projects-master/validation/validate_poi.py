#!/usr/bin/python


"""
    Starter code for the validation mini-project.
    The first step toward building your POI identifier!

    Start by loading/formatting the data

    After that, it's not our code anymore--it's yours!
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### first element is our labels, any added elements are predictor
### features. Keep this the same for the mini-project, but you'll
### have a different feature list when you do the final project.
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)

### split data into train and test sets
### 30% for testing and randdom state 42
from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=.3, random_state = 42)

### decision tree classifier
from sklearn import tree
clf = tree.DecisionTreeClassifier()

### using the full set without splitting
### accuracy score = 98.94%
# clf = clf.fit(features, labels)
# print clf.score(features, labels)

clf = clf.fit(features_train, labels_train)
pred = clf.predict(features_test)

from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
print accuracy_score(labels_test, pred)
print recall_score(labels_test, pred)
print precision_score(labels_test, pred)

### get the number of poi
count = 0
for label_test in labels_test:
    if label_test == 1:
        count += 1

print count

### get the number of people
print len(labels_test)
