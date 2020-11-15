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

def warn(*args, **kwargs):
    pass
warnings.warn = warn

def plot_heatmap(df):
    plt.title("Correlation Matrix")
    sns.heatmap(df.corr())
    plt.show()

# Load the data 
df = pd.read_csv('data.csv')

# Split into input features/output label
X = df[['subscribers', 'submission_titles_containing_toxic_words', 'submissions_containing_toxic_words', 'total_submissions_score',
        'comments_containing_toxic_words', 'total_comments_score']]
Y = df[['is_toxic']]

# Standardization
scaler = StandardScaler().fit(X)
X = scaler.transform(X)

# Train/test splitting 
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.8, random_state=0)


# plot_heatmap(df)

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
print("##Performing initial hyperparameter grid search###")
clf = GridSearchCV(
    SVC(), initial_parameters
)
clf.fit(x_train, y_train)
print(clf.best_params_)
######################################