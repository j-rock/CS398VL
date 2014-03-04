import nltk
import json
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from senti_classifier import senti_classifier as sc

stopdict = set(stopwords.words('english'))

def syn(word):
  sets = wn.synsets(word)
  if(len(sets) > 0):
    return sets[0]
  else:
    return False

def score(word):
  sy = syn(word)
  if sy:
    scores = sc.synsets_scores[sy.name]
    return scores['pos'] - scores['neg']
  else:
    return 0.0

def common(w1, w2):
  s1, s2 = syn(w1), syn(w2)
  if s1 and s2:
    lch_syns = syn(w1).lowest_common_hypernyms(syn(w2))
    if len(lch_syns) > 0:
      if len(lch_syns[0].lemmas) > 0:
        return lch_syns[0].lemmas[0].name
  return 'entity'

def getwords(filename):
  return [word for line in open(filename, 'r') for word in line.split()]

def uniqwords(chapter):
  fileIn = 'cleaned/ofk' + str(chapter) + '.txt'
  words = getwords(fileIn)
  return set([w for w in words if w not in stopdict])

def leaf(name):
  d = {}
  d['name'] = name
  d['score'] =  score(name)
  d['children'] = []
  d['parent'] = []
  return d

def bind(node, parent):
  if node['parent']:
    node['parent']['children'].remove(node)
    node['parent']['children'].append(parent)
    parent['parent'] = node['parent']
  node['parent'] = parent
  parent['children'].append(node)

def find(d, w):
  if d['name'] == w:
    return d
  else:
    for d_child in d['children']:
      match = find(d_child, w)
      if match:
        return match
  return False

def flatten(lists):
  if type(lists[0]) == dict:
    return lists
  else:
    return [l for list in lists for l in list]

def children(d):
  if len(d['children']) == 0:
    return [d]
  else:
    lists = [children(c) for c in d['children']]
    return flatten(lists)

def maxMatch(children, w):
  syw = syn(w)
  if syw:
    syns = [syn(c['name']) for c in children if syn(c['name'])]
    maxsyn = max(syns, key=syn(w).wup_similarity)
    return maxsyn.lemmas[0].name
  else:
    return False

def putInChild(d, w):
  child_name = maxMatch(d['children'], w)
  if child_name:
    c = find(d, child_name)
    if not c:
      c = d['children'][0]
    comword = common(child_name, w)
    parcomword = common(d['name'], w)
    if comword == parcomword: #no gain to be made by descending tree
      return putInLeaf(d, w)
    else:
      putInTree(c, w)
      return d
      
  else:
    return d

def putInLeaf(d, w):
  comword = common(d['name'], w)
  if comword == d['name']:
    bind(leaf(w), d)
    return d
  else:
    comnode = leaf(comword)
    bind(leaf(w), comnode)
    bind(d, comnode)
    return comnode

def putInTree(d, w):
  if len(d) == 0: ##if empty, create leaf
    return leaf(w)
  if find(d, w):  ##if already there, return
    return d
  if len(d['children']) == 0:
    return putInLeaf(d, w)
  else:
    return putInChild(d, w)

def buildTree(words):
  d = {}
  for w in words:
    d = putInTree(d, w)
  return d

def test():
  return buildTree(['dog', 'cat', 'chair', 'couch'])

def treeChapter(x):
  return buildTree(list(uniqwords(x)))

def exportTree(d):
  if d.has_key('parent'):
    d.pop('parent')
  if len(d['children']) == 0:
    d.pop('children')
    d['size'] = 1
    return d
  size = 1
  for c in d['children']:
    exportTree(c)
    size = size + c['size']
  d['size'] = size
  return d
   

l = range(1,5)
for x in range(1,5):
  fileOut = './data' + str(x) + '.json'
  tree = treeChapter(x)
  exportTree(tree)
  with open(fileOut, 'w') as outfile:
       json.dump(tree, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
  print 'Finished with Chapter ' + str(x)
