import pandas as pd
import numpy as np
import nltk
import json 
from itertools import islice
import pprint

def main():
	with(open('./yelp-dataset/yelp_academic_dataset_review.json')) as f:
		objects =(json.loads(line) for line in f)
		print(objects)
		reviews=[{}]
		i=0
		for x in objects:
			pp=pprint.PrettyPrinter(indent=4)
			print(nltk.word_tokenize(x['text']))
			#reviews.append({'business':x['business_id'],'stars':x['stars'],'text':x['text']})
			#print(reviews[i])
			i+=1
			
			#pp.pprint(reviews)


		

if __name__ == '__main__':
	main()
