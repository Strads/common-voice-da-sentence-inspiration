#%% Load packages
import requests
import zipfile
import pandas as pd
import numpy as np
import string
from nltk.stem.snowball import DanishStemmer

#%% Download files from github containing sentences
github_link = "https://raw.githubusercontent.com/common-voice/common-voice/main/server/data/da/"
files = ["europarl-v7-da.txt", "sentence-collector.txt", "singleword-benchmark.txt"]
filename = "Data/sentences.txt"

for file in files:
    r = requests.get(github_link + file)
    f = open(filename, 'a', encoding="utf-8")
    f.write(r.content.decode('utf-8'))
    f.write('\n')
    f.close()

with open(filename, "r") as file:
    data = file.read()
    sentences = data.split('\n')


#%% Get word list from DSN
RO_link = "https://dsn.dk/wp-content/uploads/2021/03/RO2012.opslagsord.med_.homnr_.og_.ordklasse.zip"
RO_filename = "Data/da_words"
r = requests.get(RO_link)
with open(RO_filename + ".zip", 'wb') as outfile:
    outfile.write(r.content)

with zipfile.ZipFile(RO_filename + ".zip","r") as zip_ref:
    zip_ref.extractall("Data")

words = pd.read_csv("Data/RO2012.opslagsord.med.homnr.og.ordklasse.txt", delimiter=';', header=None).drop(columns=[1])
words = np.unique(np.array([x.split(' ')[-1] for x in words[0]]))

pd.DataFrame(words).to_csv("Data/da_words.csv",header=None, index=None)

#%% Find words not yet used
words_used = np.unique(' '.join(sentences).translate(str.maketrans('', '', string.punctuation + '»«')).replace('– ', '').replace('— ', '').replace('\xad', '').lower().split(' '))

stemmer = DanishStemmer()
words_used_stemmed = np.unique([stemmer.stem(x) for x in words_used])
words_stemmed = np.unique([stemmer.stem(x) for x in words])

unused_words = list(set(words) - set(words_used_stemmed)- set(words_used))
unused_words.sort()

pd.DataFrame(unused_words).to_csv("Data/da_unused_words.csv",header=None, index=None)