import csv
import math
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import metrics 
from sklearn.metrics import confusion_matrix

# Reading in the data 
col_names = ['subreddit_name', 'subscribers', 'submission_titles_containing_toxic_words',
                'submissions_containing_toxic_words', 'total_submissions_score', 
                'comments_containing_toxic_words', 'total_comments_score', 'is_toxic']

data = pd.read_csv("data.csv")
data = data.dropna()

# Splitting the features and target 
features = ['subscribers', 'submission_titles_containing_toxic_words',
                'submissions_containing_toxic_words', 'total_submissions_score', 
                'comments_containing_toxic_words', 'total_comments_score']
X = data[features]
y = data.is_toxic
#print(X)
#print(y)

# Making training and test cases
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=0)

# Building the decision tree
clf = DecisionTreeClassifier(criterion="entropy", max_depth=3)
clf = clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

# Making a visual of the tree
fig, ax = plt.subplots(figsize=(20, 15))
tree.plot_tree(clf, filled=True, fontsize=10, feature_names=features)
plt.show()

# Printing out the Scores 
print("Accuracy: ", metrics.accuracy_score(y_test, y_pred))
print('Confusion Matrix: ')
print(confusion_matrix(y_test, y_pred))
