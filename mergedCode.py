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
import heapq

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
	# pp=pprint.PrettyPrinter(indent=4)
	# pp.pprint(tf_idf)
	return df,tf_idf

def score_query(query_tokens,tf_idf_store,reviews):
	queue=[]
	query_length=len(query_tokens)
	for document,content in tf_idf_store.items():
		score=0
		for word in query_tokens:
			if word in content:
				score+=tf_idf_store[document][word]
		score=score/((reviews[document]['numWords']+1)*query_length)
		if len(queue)<41:
			heapq.heappush(queue,(score,document))
		elif queue[0][0]<score:
			heapq.heappop(queue)
			heapq.heappush(queue,(score,document))
	pp=pprint.PrettyPrinter(indent=4)
	pp.pprint(queue)
	return queue


def IDF_alter(num_docs,doc_freq,token):
	'''This function gives back the idf value for a given word
		num_docs:gives the number of documents present within the corpus
		doc_freq:gives the document frequency for a given word
		token:is the token for which the inverse document frequency is to be found
	'''
	if num_docs-doc_freq[token]<=0.5*num_docs:
		return 0;#This is to make sure that idf does not give back negative values
	else:
		numer=num_docs-doc_freq[token]+0.5
		denom=doc_freq[token]+0.5
		return math.log(numer/denom)
		
def MB25Score(query_tokens,tf_idf_store,reviews,num_docs,avg_doc_length,doc_freq):
	'''This function gives the documents with the top 40 BM25 values
	query_tokens: is a list of tokens present within the query
	tf_idf_store: is a dictionary of dictionaries that contains the mapping of documents and the word:freq(word) within the document
	reviews: a dictionary that stores the document_id and related attributes
	avg_doc_length: average length of each document
	doc_freq: It is the dictionary that contains the document frequency for each word
	'''
	parameter1=1.6 #A parameter set by the designer
	parameter2=0.75 #A parameter set by the designer
	queue=[] #A queue to store the tuples of (score,document)
	for document,words in tf_idf_store.items():
		score=0
		for token in query_tokens:
			idf_val=IDF_alter(num_docs,doc_freq,token) #Get the idf value for the word
			document_length=reviews[document]['numWords'] #get the length of the document
			if(tf_idf_store[document].get(token)):
				score+=idf_val*(tf_idf_store[document][token]*(parameter1+1))/(tf_idf_store[document][token]+parameter1*(1-parameter2+parameter2*document_length/avg_doc_length))
			else:
				score=0
		if len(queue)<41:
			heapq.heappush(queue,(score,document))
		elif queue[0][0]<score:
			heapq.heappop(queue)
			heapq.heappush(queue,(score,document))
	pp=pprint.PrettyPrinter(indent=4)
	pp.pprint(queue)
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
		n=1000
		avg_doc_length=0
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
			reviews[x['review_id']]={'business':x['business_id'],'numWords':numWords,'stars':x['stars'],'text':tokens}
			avg_doc_length+=numWords
			i+=1
			print(i)
			if(i>=n):
				break
		avg_doc_length/=n
		#pp.pprint(reviews)
		doc_freq,tf_idf_store=tf_idf(reviews)      
		query=input("enter your query please")
		query_tokens=nltk.word_tokenize(query)
		query_tokens=[word.lower() for word in query_tokens if word.isalpha()]
		query_tokens=[word for word in query_tokens if not(word in stop_words)]
		query_tokens=[wordnet_lemmatizer.lemmatize(word) for word in query_tokens]
		q1=score_query(query_tokens,tf_idf_store,reviews)
		q2=MB25Score(query_tokens,tf_idf_store,reviews,n,avg_doc_length,doc_freq)
		
		with open('input_text.pickle','wb') as fp:
			pickle.dump(query,fp)
		with open('tf_out.pickle','wb') as fp:
			pickle.dump(q1,fp)
		with open('bm_out.pickle','wb') as fp:
			pickle.dump(q2,fp)
		

		#NOw pass q1,q2 to the flask GUI
if __name__ == '__main__':
	main()
