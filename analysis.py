import pickle
import nltk
import emoji
from random import randint
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer

textinput = "Just like I have the Chinese banks in my buildings, they listen to me, they respect me. China has almost complete control over North Korea. China will do that. And if they don't do that, they have to suffer economically because we have the engine that makes China work. You know, without the United States or without China sucking out all our money and our jobs China would collapse in about two minutes."

## initializers
stemmer = SnowballStemmer("english")
emojidata = pickle.load( open( "util/emoji_to_keywords.data", "rb" ) )
for emo,keys in emojidata.items():
	keys += nltk.word_tokenize( emo.replace("_"," ") )
	keys = [stemmer.stem(e) for e in keys]

## util functions
def makeEmo(emo):
	return ":"+emo+":"


tokens = nltk.word_tokenize(textinput)
tokens_stem = [stemmer.stem(e) for e in tokens]
# print tokens

result = {}
emojilist = []
for i,inputword in enumerate(tokens_stem):
	result[inputword] = []
	for emo,keys in emojidata.items():
		for key in keys:
			if inputword.lower()==key.lower():
				if emo not in emojilist: emojilist.append(makeEmo(emo))
				for j in range(0,randint(0,4)): 
					tokens.insert(i,makeEmo(emo));

## more scrabling and funzies
for i,e in enumerate(tokens):
	if randint(0,10)>8:
		for j in range(0,3):
			tokens.insert(i,emojilist[randint(0,len(emojilist)-1)])

textoutput = emoji.emojize(" ".join(tokens),use_aliases=True)

print emoji.emojize("".join(emojilist),use_aliases=True)
# print textoutput