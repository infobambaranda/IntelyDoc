from sklearn.pipeline import Pipeline
#from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn.datasets as skd

#for saving the trained module
import pickle
import os

# for SVM
from sklearn.svm import LinearSVC

# for Decision Tree
from sklearn import tree

def svm(path,categories,classifier_name,username):
    train = skd.load_files(path, categories = categories, encoding = 'ISO-8859-1')
    doc_clf = Pipeline([('tfidf', TfidfVectorizer()),
                     ('clf', LinearSVC()),
                     ])

    doc_clf.fit(train.data, train.target)

    # save the model to disk
    classifier_name = classifier_name+'.sav'
    path = 'uploads/'+username+'/classifiers/'
    if not os.path.exists(path): 
        os.makedirs(path)
    path = 'uploads/'+username+'/classifiers/'+classifier_name
    pickle.dump(doc_clf, open(path, 'wb'))

    return True

def decision_tree(path,categories,classifier_name,username):
    train = skd.load_files(path, categories = categories, encoding = 'ISO-8859-1')
    doc_clf = Pipeline([('tfidf', TfidfVectorizer()),
                     ('clf', tree.DecisionTreeClassifier()),
                     ])

    doc_clf.fit(train.data, train.target)

    doc_clf.fit(train.data, train.target)

    # save the model to disk
    classifier_name=classifier_name+'.sav'
    path = 'uploads/'+username+'/classifiers/'
    if not os.path.exists(path): 
        os.makedirs(path)
    path = 'uploads/'+username+'/classifiers/'+classifier_name
    pickle.dump(doc_clf, open(path, 'wb'))

    return True