#!flask/bin/python
from flask import Flask,request, redirect, render_template, send_from_directory, flash, Markup
import pickle
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
application = Flask(__name__)

@application.route("/")
def hello():
	return render_template('index.html')

@application.route('/', methods = ['POST'])
def signup():
	textinput = Markup("<p>"+request.form['textinput']+"</p>")

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
				
	textoutput = "".join( ("<i class='em em-" + str(e) + "'></i>" ) for e in result if result[e])

	return render_template('index.html', textoutput = Markup(textoutput) )

if __name__ == "__main__":
	application.run(host='0.0.0.0')

application.secret_key = 'bush did 9/11'
