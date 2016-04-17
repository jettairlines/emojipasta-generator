import pickle
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer

tokenizer = RegexpTokenizer(r'\w+')
emojidata = pickle.load( open( "util/emoji_to_keywords.data", "rb" ) )

textinput = "Just like I have the Chinese banks in my buildings, they listen to me, they respect me. China has almost complete control over North Korea. China will do that. And if they don't do that, they have to suffer economically because we have the engine that makes China work. You know, without the United States or without China sucking out all our money and our jobs China would collapse in about two minutes."

tokenizer = RegexpTokenizer(r'\w+')
stemmer = SnowballStemmer("english")

tokens = tokenizer.tokenize(textinput)
tokens = [stemmer.stem(e) for e in tokens]
# print tokens

for emo,keys in emojidata.items():
	keys.append(emo)
	keys = [stemmer.stem(e) for e in keys]
	

print emojidata.items()