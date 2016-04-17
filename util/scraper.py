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
	keywords = ""
	name = ""
	hexCode = ""
	foundName = False
	foundHex = False
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
			hexCode = td.contents[0]
			print "emoji unicode %s" %hexCode
			if hexCode[0:1] != "&":
				print "skipping"
				break
			if ';' in hexCode:
				hexCode = name.split(';')[0]
			foundHex = True


			if tag.getText() == "\"Short Code\" Name":
				nameList = tag.find_next_siblings("td")[0]
				if len(nameList) == 0:
					break
					name = nameList.contents[0]
					foundName = True

		if foundHex and foundKeyword:
			break

	# if len(name) != 0:
	if len(name) == 0:
		continue
	if len(keywords) > 0:
		keywordsString = keywords[0]
	else:
		if foundName:
			name = str(name.encode('utf-8'))
			str.replace(name,":","")
			print "get item with no keywords item %s" %name.lower()
			if emojiDict.get(name.lower()) == None:
				if foundHex:
					emojiDict[name.lower()] = [hexCode]
				else:
					if foundHex:
						emojiDict[name.lower()].append(hexCode)
						continue

	words = keywordsString.split(", ")
	
	print hexCode
	for word in words:
		
		if emojiDict.get(word) == None:
			emojiDict[word.lower()] = [hexCode]
		else:
			emojiDict[word.lower()].append(hexCode)
		



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
		hex_emoji = str.replace(hex_emoji," ","")
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
				print "creating new key %s and item %s" %(keyword.lower(),hex_emoji)
				emojiDict[keyword.lower()] = [hex_emoji]



dataFile = open("emoji.data",'wb')
pickle.dump(emojiDict,dataFile)
f.close()
dataFile.close()

