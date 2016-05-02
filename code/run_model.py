## Le Model

import time
import datetime
import numpy as np

from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report


np.random.seed(1339)  # for reproducibility

# Helper fns
def now():
    now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H:%M:%S')
    return str(now)

def thresholder(X, threshold):
    return X * (X > threshold)

def load_data():
    X = np.load('data/mfcc_X.npy')
    y = np.load('data/gender_y.npy')
    return X, y

print now(), ': Loading data...'
X, y = load_data()

# Feature reducer
from sklearn.decomposition import PCA
pca = PCA(n_components=50)

print now(), ': Reducing features...'
X_pca = pca.fit_transform(X)

# Split up the data
print now(), ': Splitting data...'
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.15, random_state=30)

# Train the classifiers
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

models = [SVC(), GradientBoostingClassifier()] #RandomForestClassifier(),

def get_score(X, y, model):
    acc_list, prec_list, recall_list = [],[],[]
    acc_list = cross_val_score(model, X, y, cv=5)
    prec_list = cross_val_score(model, X, y, cv=5, scoring='precision')
    recall_list = cross_val_score(model, X, y, cv=5, scoring='recall')
    print np.mean(acc_list), np.mean(prec_list), np.mean(recall_list)

print now(), ': Training models...'
for model in models:
    get_score(X_pca, y, model)




