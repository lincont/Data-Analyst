'''
Tania Lincoln
March 3, 2018

Find the features and model identifying guilty Enron employees
'''


#!/usr/bin/python

if __name__ == "__main__":
    import sys
    import pickle
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import numpy as np
    import pprint
    import pandas as pd

    from sklearn import metrics
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC, LinearSVC, NuSVC
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
    from sklearn.pipeline import Pipeline
    from sklearn.svm import SVC, LinearSVC, NuSVC
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GridSearchCV
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.decomposition import PCA
    from sklearn.feature_selection import SelectKBest
    from sklearn.preprocessing import MinMaxScaler

    sys.path.append("../../ud120-projects-master/tools/")

    from feature_format import featureFormat, targetFeatureSplit
    from tester import dump_classifier_and_data, test_classifier


    ### Load the dictionary containing the dataset
    with open("final_project_dataset.pkl", "r") as data_file:
        data_dict = pickle.load(data_file)


    ### During EDA in the Jupyter notebook,
    ### these values were found to have issues
    ### and should be removed.  Issues listed below.
    outlier_list = [
        'TOTAL',                            # outlier
        'THE TRAVEL AGENCY IN THE PARK',    # not a real person
        'LOCKHART EUGENE E',                # too many null values
        'BELFER ROBERT',                    # failed internal data integrity test
        'BHATNAGAR SANJAY']                 # failed internal data integrity test

    for k in outlier_list:
        data_dict.pop(k)


    ### helper functions to build new features
    def ratio_builder(in_value1, in_value2):
        if in_value2 == 0 or 'NaN':
            return 'NaN'
        else:
            return round(float(in_value1)/float(in_value2), 4)

    def has_value(in_value):
        if in_value != 'NaN':
            return True
        else:
            return False

    ### add new features
    for k in data_dict:
        data_dict[k]['ratio_of_to_messages_poi'] = ratio_builder(data_dict[k]['from_poi_to_this_person'], data_dict[k]['to_messages'])
        data_dict[k]['ratio_of_from_messages_poi'] = ratio_builder(data_dict[k]['from_this_person_to_poi'], data_dict[k]['from_messages'])

        # the input values will be excluded later since there are too many nulls
        # made boolean values instead, perhaps the actual values are not as important
        data_dict[k]['has_deferral_payments_bool'] = has_value(data_dict[k]['deferral_payments'])
        data_dict[k]['has_deferred_income_bool'] = has_value(data_dict[k]['deferred_income'])
        data_dict[k]['has_director_fees_bool'] = has_value(data_dict[k]['director_fees'])
        data_dict[k]['has_loan_advances_bool'] = has_value(data_dict[k]['loan_advances'])
        data_dict[k]['has_long_term_incentive_bool'] = has_value(data_dict[k]['long_term_incentive'])
        data_dict[k]['has_restricted_stock_deferred_bool'] = has_value(data_dict[k]['restricted_stock_deferred'])

    ### feature list creation
    features_list = [
        'poi',
        'salary',
        'to_messages',
        'total_payments',
        'exercised_stock_options',
        'bonus',
        'restricted_stock',
        'shared_receipt_with_poi',
        'total_stock_value',
        'expenses',
        'from_messages',
        'other',
        'from_this_person_to_poi',
        'from_poi_to_this_person',
        'has_deferral_payments_bool',
        'has_long_term_incentive_bool',
        'has_restricted_stock_deferred_bool',
        'has_loan_advances_bool',
        'has_deferred_income_bool',
        'has_director_fees_bool',
        'ratio_of_to_messages_poi',
        'ratio_of_from_messages_poi']

    for k in data_dict:
        for f in features_list:
            if data_dict[k][f] in ['NaN', None]:
                data_dict[k][f] = 0

    ### Store to my_dataset for easy export below.
    my_dataset = data_dict

    ### Extract features and labels from dataset for local testing
    data = featureFormat(my_dataset, features_list, sort_keys = True)
    labels, features = targetFeatureSplit(data)

    ### split the dataset into train and test partitions
    from sklearn.cross_validation import train_test_split
    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.3, random_state=42)

    ### Using the initial model candidate research
    ### from the Jupyter notebook, I've selected
    ### KNeighbors, SVC, and RandomForest for more investigation
    
    ### scaling used
    scalers = MinMaxScaler()

    ### reduction methods
    select_reduction = []

    pca_parameters = [
        {'reducers__n_components': [1, 2, 3, 4, 5]},]
    select_reduction.append(['pca', PCA(), pca_parameters])

    kbest_parameters = [
        {'reducers__k': [1, 2, 3, 4, 5]},]
    select_reduction.append(['kbest', SelectKBest(), kbest_parameters])


    ### build model permutation features
    candidates = []

    ### Logistic Regression
    lr_parameters = [
        {'clf__C': [1, 3, 5]},
        {'clf__n_jobs':[1,3,5,7]},]
    candidates.append(['lr', LogisticRegression(), lr_parameters])

    ### SVC
    svc_parameters = [
        {'clf__kernel' : ['rbf']}, 
        {'clf__C' : [0.025, 0.05, .5, 1]},]
    candidates.append(['svc', SVC(probability=True), svc_parameters])

    ### Random Forest
    rf_parameters = [
        {'clf__n_estimators': [10, 100, 250, 500, 1000]},
        {'clf__criterion':['gini','entropy']},
        {'clf__n_jobs':[1,3,5,7]}]
    candidates.append(['RandomForest', RandomForestClassifier(), rf_parameters])        

    ### KNN
    knn_parameters = [
        {'clf__n_neighbors': [1, 3, 5, 10, 20]},
        {'clf__n_jobs':[1,3,5,7]},]
    candidates.append(['kNN', KNeighborsClassifier(), knn_parameters])

    ### build the models
    for name, model, parameters in candidates:
        for r_name, r_model, r_parameters in select_reduction:

            # build a pipeline
            pipe = Pipeline([('scalers', scalers), ('reducers', r_model), ('clf', model)])

            # use gridsearchcv to iterate through the permutations
            grid = GridSearchCV(pipe, cv = 5, verbose = 5, scoring='accuracy', n_jobs = 5, param_grid = parameters + r_parameters)

            # train model
            clf = grid.fit(features_train, labels_train)

            # create the predictions
            predictions = clf.predict(features_test)

            # show the accuracy
            accuracy = metrics.accuracy_score(labels_test, predictions)
            print(accuracy)

    ### test the classifier
    test_classifier(clf.best_estimator_, my_dataset, features_list)

    ### export results
    dump_classifier_and_data(clf.best_estimator_, my_dataset, features_list)
    