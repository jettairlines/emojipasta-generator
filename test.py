import nltk
sentence = "Just like I have the Chinese banks in my buildings, they listen to me, they respect me. China has almost complete control over North Korea. China will do that. And if they don't do that, they have to suffer economically because we have the engine that makes China work. You know, without the United States or without China sucking out all our money and our jobs China would collapse in about two minutes."

tokens = nltk.word_tokenize(sentence)
print tokens
tagged = nltk.pos_tag(tokens)
print tagged

entities = nltk.chunk.ne_chunk(tagged)
print entities
from nltk.corpus import treebank
treebank.parsed_sents("output.mrg")[0].draw()
