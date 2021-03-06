#!flask/bin/python
from flask import Flask,request, redirect, render_template, send_from_directory, flash, Markup
import pickle
import nltk
import emoji
from random import randint
from nltk.stem.snowball import SnowballStemmer
from collections import Counter
from nltk.corpus import wordnet as wn
from nltk.stem import *
application = Flask(__name__)

@application.route("/")
def hello():
	return render_template('index.html')

@application.route('/', methods = ['POST'])
def signup():
	textinput = request.form['textinput']

	if not textinput: textinput = "@officialjaden How Can Mirrors Be Real If Our Eyes Aren't Real"


	## initializers
	stemmer = SnowballStemmer("english")
	emojidata = pickle.load( open( "util/emoji.data", "rb" ) )
	emojidata.pop(u'person',None)
	emojidata.pop(u'object',None)
	emojidata.pop(u'place',None)
	emojidata.pop(u'eyes',None)
	emojidata.pop(u'hold',None)
	emojidata.pop(u'no',None)
	emojidata.pop(u'not',None)

	for emo,keys in emojidata.items():
		emo = stemmer.stem(emo)
		keys = [stemmer.stem(e) for e in keys]

	emojidata[u'eye']=[u'&#x1F440;',u'&#x1F441']
	emojidata[u'shit']=[u'&#x1F4A9;']
	emojidata[u'loan']=[u'&#x1F911;',u'&#x1F4B0;',u'&#x1F4B4;',u'&#x1F4B5;',u'&#x1F4B8;']

	# print emojidata

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
		prob = (2 if len(tokens)>15 else 8)
		for i,e in enumerate(tokens):
			if(randint(0,10)<3):
				for j in range(0,randint(0,3)):
					tokens.insert(i+randint(0,2),emojilist[randint(0,len(emojilist)-1)])


	counts = Counter(emojilist).most_common(7);
	counts = [ e[0] for e in counts ]


	textoutput = " ".join(tokens)
	counts = " ".join(counts)
	return render_template('index.html', emojilist= Markup(counts), textoutput = Markup(textoutput) )

if __name__ == "__main__":
	application.debug = True
	application.run(host='0.0.0.0')

application.secret_key = 'bush did 9/11'
