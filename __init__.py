#!flask/bin/python
from flask import Flask,request, redirect, render_template, send_from_directory, flash, Markup
import pickle
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('index.html')

@app.route('/', methods = ['POST'])
def signup():
	textinput = Markup("<p>"+request.form['textinput']+"</p>")

	tokenizer = RegexpTokenizer(r'\w+')
	stemmer = SnowballStemmer("english")
	emojidata = pickle.load( open( "util/emoji_to_keywords.data", "rb" ) )
	for emo,keys in emojidata.items():
		keys += tokenizer.tokenize( emo.replace("_"," ") )
		keys = [stemmer.stem(e) for e in keys]

	tokens = tokenizer.tokenize(textinput)
	tokens = [stemmer.stem(e) for e in tokens]
	# print tokens

	result = []
	for inputword in tokens:
		for emo,keys in emojidata.items():
			for key in keys:
				if inputword.lower()==key.lower():
					result.append(emo)
				

	textoutput = "".join( ("<i class='em em-" + str(x) + "'></i>" ) for x in result)
	return render_template('index.html', textoutput = Markup(textoutput) )

if __name__ == "__main__":
	app.run(debug=True)

app.secret_key = 'bush did 9/11'