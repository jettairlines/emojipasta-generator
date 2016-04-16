var express = require("express");
var app     = express();
var path    = require("path");
var bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: true })); 
app.use(express.static('public'));
app.set('view engine', 'jade');


app.get('/',function(req,res){
  //res.sendFile(path.join(__dirname+'/public/index.html'));
	res.render('layout.pug');
  //__dirname : It will resolve to your project folder.
});

app.post('/', function(req, res) {

	var natural = require('natural'),
	tokenizer = new natural.WordTokenizer();

	//var input = "I also watch TV. I love Fox, I like Morning Joe, I like that the Today show did a beautiful piece on me yesterday — I mean, relatively speaking. OK, so I\'ve done all that. I then comb my hair. Yes, I do use a comb. Do I comb it forward? No, I don\'t comb it forward. I actually don\'t have a bad hairline. When you think about it, it\'s not bad. I mean, I get a lot of credit for comb-overs. But it's not really a comb-over. It\'s sort of a little bit forward and back. I\'ve combed it the same way for years. Same thing, every time."

	natural.LancasterStemmer.attach();
	var output = req.body.name.tokenizeAndStem()

	var isEmoji = require('is-emoji-keyword');
    const emojiFromWord = require("emoji-from-word");
	output.forEach(function(e,i,output){
		/*if(isEmoji(e)){
			output[i] = "HI";
		}*/
        output[i] = "<i class='em em-" + emojiFromWord(e).emoji_name + "'></i>";
	});
	
	res.render('result.pug', {emojis: output[0]});
	
	
});

app.listen(3000);

console.log("Running at Port 3000");