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
import logging
import heapq
from pathlib import Path

def calc_TF_IDF(tfval,dfval,number):
	'''
		returns the tf_idf
	'''
	return (1+math.log(tfval))*(math.log(number/dfval))

def tf_idf(reviews):
	'''This function takes a review as input and gives the tf_idf of each word for each document as the output'''
	print('TFIDF generator')
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
	file1 = open('df_store.pickle','wb')
	pickle.dump(df,file1)
	file1.close()
	file2 = open('tf_idf_store.pickle','wb')
	pickle.dump(tf_idf,file2)
	file2.close()
	return df,tf_idf

#gives the score of a query
def score_query(query_tokens,tf_idf_store,reviews):
	'''
		finds the tf_idf score of query
	'''
	queue=[]#initializing empty list for ranked retreval
	l=[]
	query_length=len(query_tokens)
	for document,content in tf_idf_store.items():
		score=0
		for word in query_tokens:#checking if each token in query is present in text
			if word in content:
				score+=tf_idf_store[document][word]
		score=score/((reviews[document]['numWords']+1)*query_length)#Normalizing cosine score
		if score>0 and len(queue)<5:#Return top 3 results
			heapq.heappush(queue,(score,document))
		elif score>0 and queue[0][0]<score:
			heapq.heappop(queue)
			heapq.heappush(queue,(score,document))
	while queue:#heapsort
		l.append(heapq.heappop(queue))
	l.reverse()
	return l


def IDF_alter(num_docs,doc_freq,token):
	'''This function gives back the idf value for a given word
		num_docs:gives the number of documents present within the corpus
		doc_freq:gives the document frequency for a given word
		token:is the token for which the inverse document frequency is to be found
	'''
	try :
		if num_docs-doc_freq[token]<=0.5*num_docs:
			return 0 #This is to make sure that idf does not give back negative values
		else:
			numer=num_docs-doc_freq[token]+0.5
			denom=doc_freq[token]+0.5
			return math.log(numer/denom)
	except:
		# print("Word not found")
		return 0

def BM25Score(query_tokens,tf_idf_store,reviews,num_docs,avg_doc_length,doc_freq):
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
	l=[]
	for document,words in tf_idf_store.items():
		score=0
		for token in query_tokens:
			idf_val=IDF_alter(num_docs,doc_freq,token) #Get the idf value for the word
			document_length=reviews[document]['numWords'] #get the length of the document
			if(tf_idf_store[document].get(token)):
				score+=idf_val*(tf_idf_store[document][token]*(parameter1+1))/(tf_idf_store[document][token]+parameter1*(1-parameter2+parameter2*document_length/avg_doc_length))
			else:
				score=0
				#push everything into a heap to get sorted output
		if len(queue)<5 and score>0:
			heapq.heappush(queue,(score,document))
		elif score>0 and queue[0][0]<score:
			heapq.heappop(queue)
			heapq.heappush(queue,(score,document))
	while queue:
		l.append(heapq.heappop(queue))
	#reverse the list since it is sorted in ascending order
	l.reverse()
	print()
	return l


def main(query):
	"""
		This function lemmatizes and normalizes all the words found in the corpus, and then calls the appropriate function to get tf_idf and BM25 scores. Then it takes the query and prints out the list of documents from both the algorithms. First the tf_idf sorted docs are printed followed by BM25 rated docs
	"""
	dict={}
	#pp=pprint.PrettyPrinter(indent=4)
	wordnet_lemmatizer=WordNetLemmatizer()#English Dictionary Lemmatizer
	stop_words=stopwords.words('english')#extracting stop words from nltk
	n=10000 #number of reviews processed
	reviews={}
	"""Will contain all the content about the reviews"""
	tf_idf_store={}#Returns the tf-idf scores of each document w.r.t each wrd
	testPath = Path(os.getcwd() + '/tf_idf_store.pickle')
	testPath1 = Path(os.getcwd() + '/df_store.pickle')
	testPath2 = Path(os.getcwd() + '/reviews.pickle')
	if testPath.is_file() and testPath1.is_file() and testPath2.is_file():
		print('exists')
		file1 = open('df_store.pickle','rb')
		doc_freq = pickle.load(file1)
		file1.close()
		file2 = open('tf_idf_store.pickle','rb')
		tf_idf_store = pickle.load(file2)
		file2.close()
		file3 = open('reviews.pickle','rb')
		xTempx = pickle.load(file3)
		avg_doc_length = xTempx['avgLength']
		reviews = xTempx['reviews']
		file3.close()
	else:
		print('not exists')
		print(testPath.is_file())
		print(testPath1.is_file())
		with(open(os.getcwd()+'/yelp_academic_dataset_review.json')) as f:
			objects =(json.loads(line) for line in f) #load the json file with reviews in it line by line because the 6GB line is too big to load in the ram at onces
			i=0
			avg_doc_length=0
			for x in objects:
				tokens=nltk.word_tokenize(x['text']) #tokenizing words
				tokens=[word.lower() for word in tokens if word.isalpha()]#Removing all punctuations and retaining only alphanumeric words
				numWords=len(tokens)#Number of words after tokenization
				tokens=[word for word in tokens if not(word in stop_words)]#Removing tokens which are stop words
				tokens=[wordnet_lemmatizer.lemmatize(word) for word in tokens]#Lemmatizing words according to their dictionary root
				reviews[x['review_id']]={'business':x['business_id'],'numWords':numWords,'stars':x['stars'],'text':tokens,'review':x['text']}
				avg_doc_length+=numWords
				i+=1
				if(i>=n):
					break
		avg_doc_length/=n
		storagecontainer = {'avgLength':avg_doc_length,'reviews':reviews}
		file1 = open('reviews.pickle','wb')
		pickle.dump(storagecontainer,file1)
		file1.close()
		doc_freq,tf_idf_store=tf_idf(reviews)#This returns the DF dict as well as TF-IDF
	#query=input("enter your query please: ")

	query=str.replace(query,'-',' ')
	query=str.replace(query,'_',' ')
	query_tokens=nltk.word_tokenize(query) #tokenizing query before searching
	query_tokens=[word.lower() for word in query_tokens if word.isalpha()]
	query_tokens=[word for word in query_tokens if not(word in stop_words)]
	query_tokens=[wordnet_lemmatizer.lemmatize(word) for word in query_tokens]
	if len(query_tokens)==0:
		query_tokens="             "
	q1=score_query(query_tokens,tf_idf_store,reviews) #q1 contains the documents ranked via tf_idf
	q2=BM25Score(query_tokens,tf_idf_store,reviews,n,avg_doc_length,doc_freq) #q2 contains the documents ranked via BM25
	results = []
	with open('id_name_mappings.pickle','rb') as nms:
		dict=pickle.load(nms)
		# "This is what Cosine Similarity returns as the most relevant documents"
		len1 = len(q1)
		if len1 == 0:
			#print("No results found")
			results.append("No results found")
		else:
			#print("Results of TF_IDF")
			results.append("Results of TF_IDF")
			for x in q1:
				#print(reviews[x[1]]['review'])
				results.append(dict[reviews[x[1]]['business']])
				results.append(reviews[x[1]]['stars'] )
				results.append(reviews[x[1]]['review'])
				#print("**************************************************************************************")
		# "This is what BM25 returns as the most relevant documents"
		len2 = len(q2)
		if len2 == 0:
			#print("No results found")
			results.append("No results found")
		else:
			#print("Results of BM25")
			results.append("Results of BM25")
			for x in q2:
				#print(reviews[x[1]]['review'])
				results.append(dict[reviews[x[1]]['business']])
				results.append(reviews[x[1]]['stars'])
				results.append(reviews[x[1]]['review'])
				#print("**************************************************************************************")


	#store the data collected so far in pickle files
	# with open('input_text.pickle','wb') as fp:
	# 	pickle.dump(query,fp)
	# with open('tf_out.pickle','wb') as fp:
	# 	pickle.dump(q1,fp)
	# with open('bm_out.pickle','wb') as fp:
	# 	pickle.dump(q2,fp)

	return results,len1,len2


if __name__ == '__main__':
	main()#Entry point for program when running directly
