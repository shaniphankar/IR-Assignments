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

def tf_idf(reviews):
	df={}
	tf_overall={}
	for document,content in reviews.items():
		if document not in tf_overall:
			tf_overall[document]=[]
			tf_doc={}
			for word in content['text']:
				if word not in tf_doc:
					if word not in df:
						df[word]=1
					else:
						df[word]=df[word]+1
					tf_doc[word]=1
				else:
					tf_doc[word]=tf_doc[word]+1
				tf_overall[document]=tf_overall[document]+[tf_doc]
	pp=pprint.PrettyPrinter(indent=4)	
	pp.pprint(tf_overall)
	print(df)	

def main():
	with(open(os.getcwd()+'/yelp-dataset/yelp_academic_dataset_review.json')) as f:
		objects =(json.loads(line) for line in f)
		print(objects)
		reviews={}
		wordnet_lemmatizer=WordNetLemmatizer()
		i=0
		for x in objects:
			pp=pprint.PrettyPrinter(indent=4)
			tokens=nltk.word_tokenize(x['text'])
			tokens=[word.lower() for word in tokens if word.isalpha()]
			numWords=len(tokens)
			stop_words=stopwords.words('english')
			#print(stop_words)
			#print(tokens)
			tokens=[word for word in tokens if not(word in stop_words)]
			tokens=[wordnet_lemmatizer.lemmatize(word) for word in tokens]
			#print(stop_words)
			#print(tokens)
			reviews[x['review_id']]={'business':x['business_id'],'numWords':numWords,'stars':x['stars'],'text':tokens}
			i+=1
			tf_idf(reviews)
			#pp.pprint(reviews)
		with open('id_tokens_mappings.pickle', 'wb') as handle:
			pickle.dump(reviews, handle, protocol=pickle.HIGHEST_PROTOCOL)
		

if __name__ == '__main__':
	main()
