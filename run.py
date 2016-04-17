#!flask/bin/python
from flask import Flask,request, redirect, render_template, send_from_directory, flash, Markup
app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('index.html')

@app.route('/', methods = ['POST'])
def signup():
    textinput = Markup("<p>"+request.form['textinput']+"</p>");
    textoutput = textinput
    return render_template('index.html', textoutput = textoutput )

if __name__ == "__main__":
    app.run(debug=True)

app.secret_key = 'bush did 9/11'