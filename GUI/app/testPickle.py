import json, pickle
output_pickle_file={}
with(open('yelp_academic_dataset_review.json','r')) as file:
    objects = (json.loads(line) for line in file)
    i = 0
    for x in objects:
        i+=1
        output_pickle_file['review ' +str(i)] = x['text']
        if i == 3:
            break
outfile = open('review_dict.pickle','wb')
pickle.dump(output_pickle_file,outfile)
outfile.close()
infile = open('review_dict.pickle','rb')
d = pickle.load(infile)
