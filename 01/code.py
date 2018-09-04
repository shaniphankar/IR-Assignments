import pandas as pd
import numpy as np
import nltk
import json 
from itertools import islice
import pprint

def main():
	with(open('./yelp-dataset/yelp_academic_dataset_review.json')) as f:
		objects =(json.loads(line) for line in f)
		objects = islice(objects,3)
		pp=pprint.PrettyPrinter(indent=4)
		pp.pprint(list(objects))

if __name__ == '__main__':
	main()
