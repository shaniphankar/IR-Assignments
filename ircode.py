import preprocess as pp 

df={}
tf_overall={}

for document in pp.doc_map:
	if document not in tf_overall:
		tf_overall[document]=[]
		tf_doc={}
		for word in pp.doc_map[document]:
			
			if word not in tf_doc:
				
				if word not in df:
					df[word]=1
				else:
					df[word]=df[word]+1

				tf_doc[word]=1

			else:
				tf_doc[word]=tf_doc[word]+1

			tf_overall[document]=tf_overall[document]+[tf_doc]

print(tf_overall)
print(df)	

			

