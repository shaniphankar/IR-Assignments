import pickle
import pprint

def main():
    with open("id_name_mappings.pickle",'rb') as fb:
        r=pickle.load(fb)
        pp=pprint.PrettyPrinter(indent=4)
        pp.pprint(r)
        # pp.pprint(r['-_BKaXQCBgupepxlv52-Qg'])

if __name__ == '__main__':
	main()
