#!flask/bin/python
from flask import Flask,request, redirect, render_template, send_from_directory, flash, Markup
import pickle
import nltk
import emoji
from random import randint
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
application = Flask(__name__)

@application.route("/")
def hello():
	return render_template('index.html')

@application.route('/', methods = ['POST'])
def signup():
	textinput = Markup("<p>"+request.form['textinput']+"</p>")

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
					for j in range(0,randint(0,3)): 
						tokens.insert(i,makeEmo(emo));

	## more scrabling and funzies
	for i,e in enumerate(tokens):
		if randint(0,10)>8:
			for j in range(0,4):
				tokens.insert(i,emojilist[randint(0,len(emojilist)-1)])

	textoutput = emoji.emojize(" ".join(tokens),use_aliases=True)

	return render_template('index.html', textoutput = Markup(textoutput) )

if __name__ == "__main__":
	application.debug = True
	application.run(host='0.0.0.0')

application.secret_key = 'bush did 9/11'
