import pickle
import nltk
import emoji
from random import randint
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet as wn
## initializers
stemmer = SnowballStemmer("english")
emojidata = pickle.load( open( "util/emoji.data", "rb" ) )
for emo,keys in emojidata.items():
	keys += nltk.word_tokenize( emo.replace("_"," ") )
	keys = [stemmer.stem(e) for e in keys]

## util functions
def makeEmo(emo):
	return ":"+emo+":"

textinput = "Just like I have the Chinese banks in my buildings, they listen to me, they respect me. China has almost complete control over North Korea. China will do that. And if they don't do that, they have to suffer economically because we have the engine that makes China work. You know, without the United States or without China sucking out all our money and our jobs China would collapse in about two minutes."
# textinput = "panda"
textoutput = textinput

tokens = nltk.word_tokenize(textinput)
tokens_stem = [stemmer.stem(e) for e in tokens]
# print tokens

result = {}
for i,inputword in enumerate(tokens_stem):
	result[inputword] = []
	print "for word %s" %inputword
	if emojidata.get(inputword.lower()) != None:
		tokens.insert(i,makeEmo(emojidata[inputword.lower()][0]))
	else:
		syns = wn.synsets(inputword)
		for syn in syns:
			
			name = syn.name().split('.')[0]
			print "found syn %s" %name
			if emojidata.get(name.lower()) != None:
				tokens.insert(i,makeEmo(emojidata[name.lower()][0]))
				break

print tokens

textoutput = emoji.emojize(" ".join(tokens))
# textoutput = "".join( ("<i class='em em-" + str(e) + "'></i>" ) for e in result if result[e])
# print result
print textoutput
