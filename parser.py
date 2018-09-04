import pickle
import json
from itertools import islice
import pprint

dict = {}

with(open('/home/addepalli/Downloads/IR1/yelp-dataset/yelp_academic_dataset_business.json')) as f:
    objects = (json.loads(line) for line in f)
    for object in objects:
        dict[object["business_id"]] = object["name"]

with open('id_name_mappings.pickle', 'wb') as handle:
    pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

# To load
# import pickle
#
# with open('id_name_mappings.pickle', 'rb') as handle:
#     dict = pickle.load(handle)
#
# print(dict["9aSMIZjC7tdXM-VyC6g0Qg"])
