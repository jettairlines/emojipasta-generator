import pickle
import nltk
import emoji
from random import randint
from nltk.corpus import wordnet as wn
from nltk.stem import *

textinput = "Just like I have the Chinese banks in my buildings, they listen to me, they respect me. China has almost complete control over North Korea. China will do that. And if they don't do that, they have to suffer economically because we have the engine that makes China work. You know, without the United States or without China sucking out all our money and our jobs China would collapse in about two minutes."

## initializers
stemmer = SnowballStemmer("english")
emojidata = pickle.load( open( "util/emoji.data", "rb" ) )
for emo,keys in emojidata.items():
	keys += nltk.word_tokenize( emo.replace("_"," ") )
	keys = [stemmer.stem(e) for e in keys]

## util functions
def makeEmo(emo):
	return ":"+emo+":"
def ngrams(input, n):
	output = {}
	for i in range(len(input)-n+1):
		g = ' '.join(input[i:i+n])
		output.setdefault(g, 0)
		output[g] += 1
 	return output

tokens = nltk.word_tokenize(textinput)
tokens_stem = [stemmer.stem(e) for e in tokens]
# print tokens
print ngrams(tokens,3)

emojilist = []
for i,inputword in enumerate(tokens_stem):
	if emojidata.get(inputword.lower()) != None:
		tokens.insert(i,makeEmo(emojidata[inputword.lower()][0]))
	else:
		syns = wn.synsets(inputword)
		for syn in syns:
			name = syn.name().split('.')[0]
			emos = emojidata.get(name.lower())
			if emos:
				for emo in emos:
					if emo not in emojilist: emojilist.append(emo)
					for j in range(0,randint(0,4)): 
						tokens.insert(i,makeEmo(emo));



# ## more scrabling and funzies
# if emojilist:
# 	emojilist = [makeEmo(e) for e in emojilist]
# 	for i,e in enumerate(tokens):
# 		if(randint(0,420)>337):
# 			for j in range(0,randint(0,3)):
# 				tokens.insert(i+randint(0,2),emojilist[randint(0,len(emojilist)-1)])

# print tokens
emojilist = emoji.emojize("".join(emojilist),use_aliases=True)
textoutput = emoji.emojize(" ".join(tokens),use_aliases=True)
# print emojilist
# print textoutput
