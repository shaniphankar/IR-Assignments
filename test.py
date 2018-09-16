import shelve

def main():
    s=shelve.open('store.db')
    for key in s:
        print(s[key]['text'])
		
if __name__ == '__main__':
	main()
