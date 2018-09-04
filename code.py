import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import json 
from itertools import islice
import pprint
import os
def main():
	with(open(os.getcwd()+'/yelp-dataset/yelp_academic_dataset_review.json')) as f:
		objects =(json.loads(line) for line in f)
		print(objects)
		reviews=[{}]
		i=0
		for x in objects:
			pp=pprint.PrettyPrinter(indent=4)
			tokens=nltk.word_tokenize(x['text'])
			tokens=[word.lower() for word in tokens if word.isalpha()]
			stop_words=stopwords.words('english')
			#print(stop_words)
			#print(tokens)
			tokens=[word for word in tokens if not(word in stop_words)]
			print(tokens)
			#print(stop_words)
			#print(tokens)
			#reviews.append({'business':x['business_id'],'stars':x['stars'],'text':x['text']})
			#print(reviews[i])
			i+=1
			#pp.pprint(reviews)

		

if __name__ == '__main__':
	main()
