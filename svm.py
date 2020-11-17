import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, accuracy_score

### CONSTANTS ######
make_heatmap = False
fine_grid_search = True
make_mean_scatter = False
####################

def warn(*args, **kwargs):
    pass
warnings.warn = warn

def plot_heatmap(df):
    plt.title("Correlation Matrix")
    sns.heatmap(df.corr())
    plt.show()

# Load the data 
df = pd.read_csv('data.csv')
df = df.dropna()

# Split into input features/output label
X = df[['subscribers', 'submission_titles_containing_toxic_words', 'submissions_containing_toxic_words', 'total_submissions_score',
        'comments_containing_toxic_words', 'total_comments_score']]
Y = df[['is_toxic']]

# Standardization
scaler = StandardScaler().fit(X)
X = scaler.transform(X)

# Train/test splitting 
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.8, random_state=0)
print('x_test ', x_test)
if make_heatmap:
    plot_heatmap(df)

#### Hyper-parameter optimization ####
initial_parameters = [
    {
        'kernel': ['linear'],
        'C': [0.1, 1, 10, 100, 1000]
    },
    {
        'kernel': ['rbf'], 
        'C': [0.5, 1, 10, 100, 1000],
        'gamma': [1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-2, 1e-1, 1],
    },
    {
        'kernel': ['poly'],
        'degree': [1, 2, 3, 4, 5, 6, 20, 50, 100],
        'gamma': [1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-2, 1e-1],
        'C': [0.5, 1, 10, 100, 1000]
    },
    {
        'kernel': ['sigmoid'],
        'C': [0.5, 1, 10, 100, 1000],
        'gamma': [1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-2, 1e-1],

    }
]
# Best parameters from the initial grid search:
# {'C': 100, 'kernel': 'linear'}
tuned_parameters = [
    {
        'kernel': ['linear'],
        'C': [30, 35, 36, 37, 38, 39, 40, 45, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 200, 400]
    }
]
# Best fine grid search parameters: 
# {'C': 35, 'kernel': 'linear'}
print("###Performing initial hyperparameter grid search###")
clf = GridSearchCV(
    SVC(), fine_grid_search and tuned_parameters or initial_parameters
)
clf.fit(x_train, y_train)
print(clf.best_params_)

print('###Grid Search Scores###')
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
if make_mean_scatter:
    plt.scatter(means, stds * 2)
    plt.title('Mean vs Std*2')
    plt.xlabel('Mean')
    plt.ylabel('Std*2')
    plt.show()

'''
    As shown in the following for loop,
    C = 35 to C = 100 have the same mean, std*2 so technically they all 
    perform the same but we will go with 35 because it is the easiest
    computationally
'''
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r"
        % (mean, std * 2, params))

print('###Classification Report###')
y_true, y_pred = y_test, clf.predict(x_test)
print(classification_report(y_true, y_pred))
print('###Confusion Matrix###')
print(confusion_matrix(y_true, y_pred))
print("###Accuracy Score###")
print(accuracy_score(y_true, y_pred))
######################################