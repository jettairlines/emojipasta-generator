import pickle
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer

tokenizer = RegexpTokenizer(r'\w+')
stemmer = SnowballStemmer("english")
emojidata = pickle.load( open( "util/emoji_to_keywords.data", "rb" ) )
for emo,keys in emojidata.items():
	keys += tokenizer.tokenize( emo.replace("_"," ") )
	keys = [stemmer.stem(e) for e in keys]

# print emojidata.items()

textinput = "Just like I have the Chinese banks in my buildings, they listen to me, they respect me. China has almost complete control over North Korea. China will do that. And if they don't do that, they have to suffer economically because we have the engine that makes China work. You know, without the United States or without China sucking out all our money and our jobs China would collapse in about two minutes."
# textinput = "panda"
textoutput = textinput

tokens = tokenizer.tokenize(textinput)
tokens = [stemmer.stem(e) for e in tokens]
# print tokens

result = {}
for inputword in tokens:
	result[inputword] = []
	for emo,keys in emojidata.items():
		for key in keys:
			if inputword.lower()==key.lower():
				result[inputword].append(emo);


			
# textoutput = "".join( ("<i class='em em-" + str(e) + "'></i>" ) for e in result if result[e])
print result
# print textoutput