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
		
def MB25Score(query_tokens,tf_idf_store,reviews,avg_doc_length,doc_freq):
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
			document_length=len(reviews[document]['text']) #get the length of the document
			score+=idf_val*(tf_idf_store[document][token]*(parameter1+1))/(tf_idf_store[document][token]+parameter1*(1-parameter2+parameter2*document_length/avg_doc_length))
			
		if len(queue)<41:
			heapq.heappush(queue,(score,document))
		elif queue[0][0]<score:
			heapq.heappop(queue)
			heapq.heappush(queue,(score,document))
		
	return queue