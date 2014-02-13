import nltk
import json

from nltk.book import FreqDist
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords

wordlists = PlaintextCorpusReader('', 'ofkc[1234]\.txt')
stop = stopwords.words('english')
stopdict = dict(zip(stop, stop))

def makeDict(x):
  fileIn = 'cleaned/ofk' + str(x) + '.txt'
  words = [w for w in wordlists.words(fileIn) if w not in stopdict]
  freq = FreqDist(words)
  len = float(freq.N())
  return [dict(word=w,freq=(freq[w])/len, ch=x) for w in freq]

l = range(1,5)
for x in range(1,5):
  l[x-1] = makeDict(x)
  
table = [item for sublist in l for item in sublist]
fileOut = './data.json'
with open(fileOut, 'w') as outfile:
     json.dump(table, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
