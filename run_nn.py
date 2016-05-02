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

def load_data():
    X = np.load('data/mfcc_X.npy')
    y = np.load('data/gender_y.npy')
    return X, y

def save_model(model):
    json_string = model.to_json()
    open('data/model_arch.json', 'w').write(json_string)
    model.save_weights('data/model_wgts.h5')

# Build the NN
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation

# for a single-input model with 2 classes (binary):
print now(), ': Loading model...'
model = Sequential()
model.add(Dense(1, input_dim=5504, activation='sigmoid'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

print now(), ': Loading data...'
X, y = load_data()
print now(), ': Splitting data...'
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=60)

# train the model, iterating on the data in batches of 32 samples
print now(), ': Fitting model...'
model.fit(X_train, y_train, nb_epoch=100, batch_size=32)

print now(), ': Saving model...'
save_model(model)

score = model.evaluate(X_test, y_test, batch_size=32)
print now(), ': Final Score:'
print score