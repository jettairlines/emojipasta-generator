#!flask/bin/python
from flask import Flask,request, redirect, render_template, send_from_directory, flash
import pickle
import nltk
import emoji
from random import randint
from nltk.corpus import wordnet as wn
from nltk.stem import *
application = Flask(__name__)

@application.route("/")
def hello():
	return render_template('index.html')

@application.route('/', methods = ['POST'])
def signup():
	textinput = request.form['textinput']

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
	ngramz = ngrams(tokens,4).keys()

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


	## more scrabling and funzies
	if ngramz and len(textinput)<150:
		for i,e in enumerate(tokens):
			if(randint(0,420)>337):
				tokens.insert(i+randint(0,2),ngramz[randint(0,len(ngramz)-1)])

	if emojilist:
		emojilist = [makeEmo(e) for e in emojilist]
		for i,e in enumerate(tokens):
			if(randint(0,420)>337):
				for j in range(0,randint(0,3)):
					tokens.insert(i+randint(0,2),emojilist[randint(0,len(emojilist)-1)])


	textoutput = emoji.emojize(" ".join(tokens),use_aliases=True)
	emojilist = emoji.emojize("".join(emojilist),use_aliases=True)
	return render_template('index.html', emojilist= emojilist, textoutput = textoutput )

if __name__ == "__main__":
	application.debug = True
	application.run(host='0.0.0.0')

application.secret_key = 'bush did 9/11'
