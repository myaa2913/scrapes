import sys
from lxml import html
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
from random import randint
import numpy as np
import os.path
import bs4
import csv
import pandas as pd
import time

def main():
	#get userIDs and names
	colnames=['userID', 'name']
	df=pd.read_csv("Users10k.csv", names=colnames, sep='\t')
	userIDs=list(df.userID)
	names=list(df.name)
	#print(userIDs)
	#print(names)

	scrape(userIDs,names)


def scrape(x,y):
	for i in range(0, 198):	
		page=1
		
		#clear variable lists
		#bTitle=[]
		bURL=[]
		bRating=[]
		bUserID=[]
		bAdded=[]
		bReview=[]
		#bNames=[]
		
		#grab current user
		userID=x[i]
		print(userID)
		#name=y[i]
		#print(name)
				
		#grap page 1
		time.sleep(2)
		url="https://www.goodreads.com/review/list/"+str(userID)+"?page="+str(page)+"&print=true&shelf=read"
		response=urllib.request.urlopen(url).read()
		soup=BeautifulSoup(response)
		#check for restricted profile
		public=restrictedCheck(soup)
		
		if public:
			#find current and max page
			title=soup.title.string.split()
			totalMax=title[-5].replace(")","")
			print(totalMax)
			currentMax=title[-7].split("-")[-1]
			print(currentMax)

			while currentMax!=totalMax: 
				#grab book titles/URLs/ 
				t1=soup.findAll("td", { "class" : "field title" })
				for i in t1:
					#bTitle.append(i.a['title'])
					bURL.append(i.a['href'])
				del t1
				
				#grab user rating
				t1=soup.findAll("td", { "class" : "field rating" })
				for i in t1:
					bRating.append(i.a.string[0])
					bUserID.append(userID)
					#bNames.append(name)
				del t1
				
				#grab date added
				t1=soup.findAll("td", { "class" : "field date_added" })
				for i in t1:
					bAdded.append(i.span['title'])
				del t1
				
				#grab book review
				t1=soup.findAll("td", { "class" : "field review" })
				for i in t1:
					if (i.span.string is None):
						bReview.append(i.span.string)
					else: 
						bReview.append(i.span.string.encode('utf8', 'ignore'))
				del t1
				
				#advance page counter
				page+=1
				
				time.sleep(2)
				url="https://www.goodreads.com/review/list/"+str(userID)+"?page="+str(page)+"&print=true&shelf=read"
				response=urllib.request.urlopen(url).read()
				soup=BeautifulSoup(response)
				
				title=soup.title.string.split()
				totalMax=title[-5].replace(")","")
				print(totalMax)
				currentMax=title[-7].split("-")[-1]
				print(currentMax)

			
			if currentMax==totalMax:	
				#grab book titles/URLs/ 
				t1=soup.findAll("td", { "class" : "field title" })
				for i in t1:
					#bTitle.append(i.a['title'])
					bURL.append(i.a['href'])
				del t1
					
				#grab user rating
				t1=soup.findAll("td", { "class" : "field rating" })
				for i in t1:
					bRating.append(i.a.string[0])
					bUserID.append(userID)
					#bNames.append(name)
				del t1
				
				#grab date added
				t1=soup.findAll("td", { "class" : "field date_added" })
				for i in t1:
					bAdded.append(i.span['title'])
				del t1
				
				#grab book review
				t1=soup.findAll("td", { "class" : "field review" })
				for i in t1:
					if (i.span.string is None):
						bReview.append(i.span.string)
					else: 
						bReview.append(i.span.string.encode('utf8', 'ignore'))
				del t1
				
			print("DONE")
			
			writer=csv.writer(open("data.csv", "a"))
			rows=zip(bURL,bRating,bUserID,bAdded,bReview)
			for row in rows:
				writer.writerow(row)
			

def restrictedCheck(x):
	y=x.find("div", { "id" : "privateProfile" })
	if y: 
		return False
	else:
		return True
		

	
if __name__ == '__main__':
	main()
	
