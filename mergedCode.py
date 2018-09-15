import pandas as pd
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import json 
from itertools import islice
import pprint
import os
import pickle
import math
import shelve
import pymongo
import logging


def calc_TF_IDF(tfval,dfval,number):
	return (1+math.log(tfval))*(math.log(number/dfval))

def tf_idf(reviews):
	'''This function takes a review as input and gives the tf_idf of each word for each document as the output'''
	df={} #dictionary to hold word:document frequency
	tf_overall={} #holds the tf for each word within a document 
	number=0
	for document,content in reviews.items():
		number+=1
		if document not in tf_overall:
			tf_overall[document]={}
			tf_doc={} #temp tf for each document
			for word in content['text']:
				if word not in tf_doc: #checking for the first instance of a word
					if word not in df:
						df[word]=1
					else:
						df[word]=df[word]+1
					tf_doc[word]=1
				else:
					tf_doc[word]=tf_doc[word]+1

				tf_overall[document][word]=tf_doc[word] #Adding the list of word:freq dictionaries
	tf_idf={}
	for document,content in reviews.items():
		if document not in tf_idf:
			tf_idf[document]={} #mapping each tf_idf to the corresponding document
			tf_idf_doc={} #give the tf_idf for each word in a document
			for word in content['text']:
				val=calc_TF_IDF(tf_overall[document][word],df[word],number)
				tf_idf_doc[word]=val
				tf_idf[document][word]=tf_idf_doc[word]

	#print(tf_idf)
	return tf_idf

def score_query(query_tokens,tf_idf_store):
	queue=[]
	for document,content in tf_idf_store.items():
		score=0
		for word in query_tokens:
			if word in content:
				score+=tf_idf_store[document][word]
		if len(queue)<41:
			heapq.heappush(queue,(score,document))
		elif queue[0][0]<score:
			heapq.heappop(queue)
			heapq.heappush(queue,(score,document))
	return queue

def main():
	myclient=pymongo.MongoClient('localhost', 27017)
	db=myclient.test_database
	collection=db.test_collection
	with(open(os.getcwd()+'/yelp-dataset/yelp_academic_dataset_review.json')) as f:
		objects =(json.loads(line) for line in f)
		#print(objects)
		reviews={}
		tf_idf_store={}
		pp=pprint.PrettyPrinter(indent=4)
		stop_words=stopwords.words('english')
		wordnet_lemmatizer=WordNetLemmatizer()
		i=0
		for x in objects:
			tokens=nltk.word_tokenize(x['text'])
			tokens=[word.lower() for word in tokens if word.isalpha()]
			numWords=len(tokens)
			#print(stop_words)
			#print(tokens)
			tokens=[word for word in tokens if not(word in stop_words)]
			tokens=[wordnet_lemmatizer.lemmatize(word) for word in tokens]
			#print(stop_words)
			#print(tokens)
			d={x['review_id']:{'business':x['business_id'],'numWords':numWords,'stars':x['stars'],'text':tokens}}
			collection.insert(d)
			print(i)
			i+=1
			#pp.pprint(reviews)
		# tf_idf_store=tf_idf(reviews)      
		# query=input("enter your query please")
		# query_tokens=nltk.word_tokenize(query)
		# query_tokens=[word.lower() for word in query_tokens if word.isalpha()]
		# query_tokens=[word for word in query_tokens if not(word in stop_words)]
		# query_tokens=[wordnet_lemmatizer.lemmatize(word) for word in query_tokens]
		# score_query(query_tokens,tf_idf_store)

		
if __name__ == '__main__':
	main()
