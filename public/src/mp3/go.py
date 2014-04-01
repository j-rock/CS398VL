import nltk
import json
import re, pprint

namesets = [{'Name':"DUMMY", 'Set':set()}
           ,{'Name':"Sir Arthur", 'Set':set(["Sir Arthur", "arthur"])}
           ,{'Name':"Sir Lancelot", 'Set':set(["Sir Lancelot", "lancelot"])}
           ,{'Name':"Merlyn", 'Set':set(["Merlyn", "merlyn"])}
           ,{'Name':"Wart", 'Set':set(["Wart", "wart"])}
           ,{'Name':"Guenever", 'Set':set(["Guenever", "guenever"])}
           ,{'Name':"Sir Mordred", 'Set':set(["Sir Mordred", "mordred"])}
           ,{'Name':"Morgause", 'Set':set(["Morgause", "morgause"])}
           ,{'Name':"Elaine", 'Set':set(["Elaine", "elaine"])}
           ,{'Name':"Sir Galahad", 'Set':set(["Galahad", "galahad"])}
           ,{'Name':"Sir Gareth", 'Set':set(["Sir Gareth", "gareth"])}
           ,{'Name':"Sir Gawaine", 'Set':set(["Sir Gawaine", "gawaine"])}
           ,{'Name':"King Pellinore", 'Set':set(["King Pellinore", "pellinore"])}
           ,{'Name':"Sir Kay", 'Set':set(["Sir Kay", "kay"])}
           ,{'Name':"Sir Ector", 'Set':set(["Sir Ector", "ector"])}
           ,{'Name':"The Questing Beast", 'Set':set(["The Questing Beast", "questingbeast"])}
           ,{'Name':"Sir Agravaine", 'Set':set(["Sir Agravaine", "agravaine"])}
           ,{'Name':"Sir Bruce", 'Set':set(["Sir Bruce", "bruce"])}
           ,{'Name':"Uncle Dap", 'Set':set(["Uncle Dap", "dap"])}
           ,{'Name':"Morgan le Fay", 'Set':set(["Morgan le Fay", "morgan"])}
           ,{'Name':"Nimue", 'Set':set(["Nimue", "nimue"])}
           ,{'Name':"Sir Thomas Malory", 'Set':set(["Sir Thomas Malory", "tom", "thomas", "malory"])}
           ,{'Name':"King Uther Pendragon", 'Set':set(["King Uther Pendragon", "uther", "pendragon"])}
           ]

friendsets = [{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ,{}
             ]


def findSet(nsets, word):
  size = len(nsets)
  for i in range(0, size):
    if(word in nsets[i]['Set']):
      return i
  return False

def addFriend(nsets, currentSet, friendSets, word):
  set = findSet(nsets, word)
  if set and (set != currentSet):
    properName = nsets[set]['Name']
    if properName in friendSets[currentSet]:
      friendSets[currentSet][properName] += 1
    else:
      friendSets[currentSet][properName] = 1

def getwords(filename):
  raw_text = open(filename).read()
  tokens_raw = nltk.word_tokenize(raw_text)
  tokens_lower = [w.lower() for w in tokens_raw]
  tokens_punct = [re.sub('\.','',w) for w in tokens_lower]
  return [w for w in tokens_punct if w.isalpha()] 


def letsgo(words, nsets, fsets, neighborCount):
  nwords = len(words)
  for i in range(0, nwords):
    word = words[i]
    set = findSet(nsets, word)
    if set:
      neighborhood = words[i-neighborCount : i+neighborCount]
      for w in neighborhood:
        addFriend(nsets, set, fsets, w)


def nvpairs(nsets):
  return [{'name' : pair['Name']} for pair in nsets[1:]]

def expfriends(nsets, fsets):
  lists = groupfriends(nsets, fsets)
  return [item for list in lists for item in list]

def groupfriends(nsets, fsets):
  size = len(fsets)
  return [helper(i-1, nsets, fsets[i]) for i in range(1,size)]

def helper(sourceI, nsets, fset):
    return [{'source':sourceI, 'target':(findSet(nsets,name)-1), 'value':fset[name]} for name in fset.keys() if (sourceI < (findSet(nsets,name)-1))]

def doit(neighborsize):
  letsgo(getwords('ofk.txt'), namesets, friendsets, neighborsize)

doit(10)

fileOut = 'data.json'
out = {}
out['nodes'] = nvpairs(namesets)
out['links'] = expfriends(namesets, friendsets)
with open(fileOut, 'w') as outfile:
     json.dump(out, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
