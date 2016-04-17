import numpy as np
from lxml import html
import requests
from bs4 import BeautifulSoup
import pickle

links = []
linksToScrape = ["http://www.iemoji.com/meanings-gallery/people","http://www.iemoji.com/meanings-gallery/places","http://www.iemoji.com/meanings-gallery/nature","http://www.iemoji.com/meanings-gallery/objects","http://www.iemoji.com/meanings-gallery/symbols","http://www.iemoji.com/meanings-gallery/new"]#,"http://www.iemoji.com/meanings-gallery/skin-tones"]
for linkToScrape in linksToScrape:
	page = requests.get(linkToScrape)
	bs = BeautifulSoup(page.content,"lxml")
	possible_links = bs.find_all('a')
	for link in possible_links:
		if link.has_attr('href'):
			attr = link.attrs['href']
			firstFourAttr = attr[0:5]
			
			if firstFourAttr == '/view':
				links.append("http://www.iemoji.com"+link.attrs['href'])


print "complete scraping links"
emojiDict = {}
f = open("output.txt",'w')
for link in links:
	page = requests.get(link)
	bs = BeautifulSoup(page.content,"lxml")
	possible_tags = bs.find_all('td')
	print link
	keywords = ""
	name = ""
	foundName = False
	foundKeyword = False
	for tag in possible_tags:
		if tag.getText() == "Keywords":
			keywords = tag.find_next_siblings("td")[0].contents
			if len(keywords) == 0: 
				break
			foundKeyword = True

		if tag.getText() == "Hexadecimal HTML Entity":
			tds = tag.find_next_siblings("td")
			td = tds[len(tds)-1]
			#if len(nameList) == 0:
			#	break
			
			name = td.contents[0]
			if ';' in name:
				name = name.split(';')[0]
			foundName = True

		if foundName and foundKeyword:
			break

	# if len(name) != 0:
	if len(name) == 0:
		continue
	if len(keywords) > 0:
		keywordsString = keywords[0]
	else:
		
		if emojiDict.get(name.lower()) == None:
			emojiDict[name.lower()] = [name]
		else:
			emojiDict[name.lower()].append(name)
		continue

	words = keywordsString.split(", ")
	
	print name
	for word in words:
		
		f.write("%s,%s\n" %(word.encode('utf-8'),name.encode('utf-8')))
		if emojiDict.get(word) == None:
			emojiDict[word.lower()] = [name]
		else:
			emojiDict[word.lower()].append(name)
		



page = requests.get("http://unicode.org/emoji/charts/full-emoji-list.html")
bs = BeautifulSoup(page.content,"lxml")
possible_links = bs.find_all('tr')
for link in possible_links:
	hex_emoji = "" 
	possible_code_td = link.find_all('td',{ "class" : "code" })
	for td in possible_code_td:
		td.find("a",recursive=False)
		hex_emoji = td.getText()
		hex_emoji = str.replace(str(hex_emoji),"U+","&#x").lower()
		print hex_emoji

	possible_name_td = link.find_all('td',{ "class" : "name" })
	for td in possible_name_td:
		td.find("a",recursive=False)
		name = td.getText()
		
		keywords = name.split(", ")
		for keyword in keywords:
			if emojiDict.get(keyword.lower()) != None:
				print "key %s appended %s" %(keyword.lower(),hex_emoji)
				emojiDict[keyword.lower()].append(hex_emoji)
			else:
				print "creating new key %s and item %s" %(name.lower(),hex_emoji)
				emojiDict[keyword.lower()] = [hex_emoji]



dataFile = open("emoji.data",'wb')
pickle.dump(emojiDict,dataFile)
f.close()
dataFile.close()

