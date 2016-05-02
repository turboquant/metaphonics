from bs4 import BeautifulSoup
import requests
import os

import time
import random
import datetime

import cPickle as pickle

data_store = {}

def lang_assign():
    '''create dictionary for looking up the family of every given native language
    languages here were chosen because they had the most recordings available, or for the purpose of adding to the minority classes'''

    euro = ['italian', 'macedonian', 'swedish', 'romanian', 'serbian', 'bulgarian']
    euro = ['english', 'spanish', 'french', 'portuguese', 'russian', 'dutch', 'german', 'polish', 'italian', 'macedonian', 'swedish', 'romanian', 'serbian', 'bulgarian']
    indo = ['persian', 'hindi', 'urdu', 'bengali', 'nepali', 'kurdish', 'punjabi', 'pashto', 'gujarati', 'dari', 'sinhalese']
    sino = ['cantonese', 'gan', 'hainanese', 'hakka', 'mandarin', 'naxi', 'taiwanese', 'teochew', 'wu', 'xiang', 'burmese', 'tibetan']
    afro = ['arabic', 'amharic', 'hausa', 'hebrew', 'tigrigna', 'somali']

    result = {}
    for lang in euro:
        result[lang] = 'european'
    for lang in indo:
        result[lang] = 'indo_iranian'
    for lang in sino:
        result[lang] = 'sino_tibetan'
    for lang in afro:
        result[lang] = 'afroasiatic'
    return result

def get_language_urls(index, language):
    '''generate a list of the urls needed to scrape the mp3s for a given language'''

    urls_to_scrape = (index + 'browse_language.php?function=find&language=' + language)
    data_store['urls_to_scrape'] = urls_to_scrape
    return urls_to_scrape

def get_speaker_info(index, url):
    '''generate a list of tuples which contain all the relevant information for the speakers of a given language'''
    
    def get_meta(p):
        '''retrieve meta data on a given speaker (country of origin and gender)'''

        meta = str(p).split('</a>')[-1].strip('</p>')
        meta = meta.strip(',').split()
        org = meta[-1]
        gender = meta[0][0]
        return org, gender

    speakers = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    content = soup.find(class_='content')
    for p in content.find_all('p'):
        org, gender = get_meta(p)
        speakers.append((index + p.find('a')['href'], gender, org))

    data_store['speakers'] = speakers
    return speakers

def get_audio(index, speakers, language, directory):
    '''download the audio files for a given language into the given directory'''

    audio = []
    for speaker in speakers[0:80]:
        r = requests.get(speaker[0])
        soup = BeautifulSoup(r.content)
        content = soup.find(class_='content')
        source = soup.find('source')['src']
        source = source.split('/')
        source = index + source[-2] + '/' + source[-1]

        # set the fname for each mp3 to be this format: gender_orgcountry_speakerid.mp3
        fname = speaker[1] + '_' + speaker[2] + '_' + source.split('/')[-1]
        
        audio.append((source, fname))
        print 'Getting audio: {}'.format(str(fname))


    print len(audio)
    # data_store['audio'] = audio
    # save_data(data_store)

    print 'Data stored. Retrieving now.'
    raw_input("Press Enter to continue...")

    new_source = 'http://chnm.gmu.edu/accent/soundtracks/' + 'spanish1.mp3'

    os.makedirs(directory)
    os.chdir(directory)
    for mp3 in audio:
        source = mp3[0]
        fname = mp3[1]
        grabThis = 'wget -O ' + fname + ' ' + source # for linux
        os.system(grabThis)

def now():
    now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
    return str(now)

def save_data(data):
    datafile = 'data_store_{}.pkl'.format(now())
    with open(datafile, 'wb') as fp:
        pickle.dump(data, fp)

if __name__ == '__main__':

    lang_fam = lang_assign()

    index = 'http://accent.gmu.edu/'

    for lang, fam in lang_fam.iteritems():
        directory = 'audio_data/' + fam + '/' + lang + '/'

        print 'working on - ', lang

        urls_to_scrape = get_language_urls(index, lang)
        speakers = get_speaker_info(index, urls_to_scrape)
        get_audio(index, speakers, lang, directory)