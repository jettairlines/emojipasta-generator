from nltk.twitter import Twitter

i = 0
dir = "/Users/oskarzhang/twitter-files/"
#sent_tokenizer = nltk.RegexpTokenizer("")
#while(i < 1000):	i += 1
tw = Twitter()
tw.tweets(limit = 1000)
	
