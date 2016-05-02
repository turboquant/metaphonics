## Le Featurizer

import os
import time
import numpy as np

import librosa
from sklearn.decomposition import PCA


def list_files(lang_list):
    results = []
    for lang in lang_list:
        myfiles = os.listdir(lang)
        for mp3 in myfiles:
            if '.mp3' in mp3:
                results.append([lang, mp3])
            else:
                pass
    return results

def prep_data(obs_list):
    raw_data = {}
    for obs_dir, obs_mp3 in obs_list:
        # Load data from audio file
        y, sr = librosa.load(obs_dir + obs_mp3, sr=44100, duration=18)

        # Make a mel-scaled power (energy-squared) spectrogram
        S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)

        # Convert to log scale (dB). We'll use the peak power as reference.
        log_S = librosa.logamplitude(S, ref_power=np.max) + 80 # 80 to make positive

        key = obs_mp3.split('.mp3')[0]
        gender, country = obs_mp3.split('_')[0:2]

        # Store into a data dict
        raw_data[key] = {'y': y, 'sr': sr, 'S': S, 'log_S': log_S, 'gender': gender, 'country': country}
    
    return raw_data

def labeled_data(raw_data):
    X, y = [],[]
    for k, v in raw_data.iteritems():
        # remove short obs
        if v['log_S'].shape[1] == 1551:
            X.append(v['log_S'])
            y.append(v['gender'] == 'f')
    y = map(lambda x: 1 if x else 0, y)
    return X, y

def expand_data(X, y):
    exp_X, exp_y = [], []
    for i, obs in enumerate(X):
        tmpX, tmpy = chop_obs2(obs, y[i])
        exp_X.append(tmpX)
        exp_y.append(tmpy)
    return np.vstack(exp_X), np.vstack(exp_y).flatten()

def chop_obs2(obs, label):
    result, y = [], []
    for i in xrange(3, obs.shape[1], 43):
        start = i
        stop = i + 43
        result.append(obs[:,start:stop].flatten())
        y.append(label)
    return np.vstack(result), np.stack(y)

def chop_obs(obs):
    result = []
    for i in xrange(3, obs.shape[1], 43):
        start = i
        stop = i + 43
        result.append(obs[:,start:stop].flatten())
    return np.vstack(result)

def reduce_data_pca(X):
    pca = PCA(n_components=100)
    X_pca = pca.fit_transform(X)
    return X_pca

def export_npy(X, y):
    np.save('mfcc_X.npy', X)
    np.save('gender_y.npy', y)
    print 'X: {}, y: {}\nFiles saved.'.format(X.shape, y.shape)

## Main runs here
if __name__ == '__main__':

    use_these = ['audio_data/european/spanish/',
                 'audio_data/european/french/',
                 'audio_data/european/dutch/',
                 'audio_data/european/swedish/',
                 'audio_data/european/italian/',
                 'audio_data/european/english/']

    obs = list_files(use_these)
    raw_X = prep_data(obs)
    Xtmp, ytmp = labeled_data(raw_X)
    X, y = expand_data(Xtmp, ytmp)
    
    # X_pca = reduce_data(X)
    export_npy(X, y)







