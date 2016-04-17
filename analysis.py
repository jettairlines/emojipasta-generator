import pickle
import nltk
import emoji
from random import randint
from nltk.stem.snowball import SnowballStemmer
from collections import Counter
from nltk.corpus import wordnet as wn
from nltk.stem import *

textinput = "Just like I have the Chinese banks in my buildings, they listen to me, they respect me. China has almost complete control over North Korea. China will do that. And if they don't do that, they have to suffer economically because we have the engine that makes China work. You know, without the United States or without China sucking out all our money and our jobs China would collapse in about two minutes."

## initializers
stemmer = SnowballStemmer("english")
emojidata = pickle.load( open( "util/emoji.data", "rb" ) )
for emo,keys in emojidata.items():
	keys += nltk.word_tokenize( emo.replace("_"," ") )
	keys = [stemmer.stem(e) for e in keys]

emojidata.pop(u'person',None)
emojidata.pop(u'object',None)
emojidata.pop(u'place',None)
emojidata.pop(u'eyes',None)
# emojidata[u'eyes']=["&#x1F440;"]

print emojidata


## util functions
def ngrams(input, n):
	output = {}
	for i in range(len(input)-n+1):
		g = ' '.join(input[i:i+n])
		output.setdefault(g, 0)
		output[g] += 1
	return output

tokens = nltk.word_tokenize(textinput)
tokens_stem = [stemmer.stem(e) for e in tokens]
ngramz = ngrams(tokens,5).keys()

emojilist = []
for i,inputword in enumerate(tokens_stem):
	if emojidata.get(inputword.lower()) != None:
		emos = emojidata[inputword.lower()]
		tokens.insert(i,emos[randint(0,len(emos)-1)])
	else:
		syns = wn.synsets(inputword)
		for syn in syns:
			name = syn.name().split('.')[0]
			if emojidata.get(name.lower()) != None:
				emos = emojidata[name.lower()]
				if emos:
					for emo in emos:
						if emo not in emojilist: 
							emojilist.append(emo)
					for j in range(0,randint(1,5)): 
						tokens.insert(i,emos[randint(0,len(emos)-1)]);



if ngramz:
	prob = (2 if len(tokens)>20 else 4)
	for i,e in enumerate(tokens):
		if(randint(0,10)<prob):
			tokens.insert(i+randint(0,2),ngramz[randint(0,len(ngramz)-1)])

if emojilist:
	prob = (2 if len(tokens)>15 else 6)
	for i,e in enumerate(tokens):
		if(randint(0,10)<3):
			for j in range(0,randint(0,3)):
				tokens.insert(i+randint(0,2),emojilist[randint(0,len(emojilist)-1)])


counts = Counter(emojilist).most_common(7);
counts = [ e[0] for e in counts ]

# print emojilist
# print textoutput
