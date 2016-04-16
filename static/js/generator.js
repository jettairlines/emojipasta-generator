var natural = require('natural'),
tokenizer = new natural.WordTokenizer();

var input = "I also watch TV. I love Fox, I like Morning Joe, I like that the Today show did a beautiful piece on me yesterday — I mean, relatively speaking. OK, so I\'ve done all that. I then comb my hair. Yes, I do use a comb. Do I comb it forward? No, I don\'t comb it forward. I actually don\'t have a bad hairline. When you think about it, it\'s not bad. I mean, I get a lot of credit for comb-overs. But it's not really a comb-over. It\'s sort of a little bit forward and back. I\'ve combed it the same way for years. Same thing, every time."

natural.LancasterStemmer.attach();
var output = input.tokenizeAndStem()

var isEmoji = require('is-emoji-keyword');
output.forEach(function(e,i,output){
	if(isEmoji(e)){
		output[i] = "HI";
	}
});