#!flask/bin/python
from flask import Flask,request, redirect, render_template, send_from_directory, flash, Markup
import pickle
import nltk
import emoji
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
application = Flask(__name__)

@application.route("/")
def hello():
	return render_template('index.html')

@application.route('/', methods = ['POST'])
def signup():
	textinput = Markup("<p>"+request.form['textinput']+"</p>")

	stemmer = SnowballStemmer("english")
	emojidata = pickle.load( open( "util/emoji_to_keywords.data", "rb" ) )
	for emo,keys in emojidata.items():
		keys += nltk.word_tokenize( emo.replace("_"," ") )
		keys = [stemmer.stem(e) for e in keys]

	# print emojidata.items()

	textinput = "Just like I have the Chinese banks in my buildings, they listen to me, they respect me. China has almost complete control over North Korea. China will do that. And if they don't do that, they have to suffer economically because we have the engine that makes China work. You know, without the United States or without China sucking out all our money and our jobs China would collapse in about two minutes."
	# textinput = "panda"
	textoutput = textinput

	tokens = nltk.word_tokenize(textinput)
	tokens_stem = [stemmer.stem(e) for e in tokens]
	# print tokens

	result = {}
	for i,inputword in enumerate(tokens_stem):
		result[inputword] = []
		for emo,keys in emojidata.items():
			for key in keys:
				if inputword.lower()==key.lower():
					tokens.insert(i,":"+emo+":");

	# print tokens

	textoutput = emoji.emojize(" ".join(tokens))

	return render_template('index.html', textoutput = Markup(textoutput) )

if __name__ == "__main__":
	application.run(host='0.0.0.0')

application.secret_key = 'bush did 9/11'
