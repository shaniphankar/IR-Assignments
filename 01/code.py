import sqlite3
import numpy as np
import nltk

def exec(conn,query):
	c=conn.cursor()
	c.execute(query)
	res=c.fetchall()
	c.close()
	conn.commit()
	return res

def main():
	conn=sqlite3.connect('01/database.sqlite')
	# query="""select name from sqlite_master where type = 'table';"""
	# print(exec(conn,query))
	# #It contatins 1 table called Reviews
	# query="""select * from Reviews limit 5"""
	# print(exec(conn,query))
	query="select text from Reviews;"
	rows_text=exec(conn,query)
	rows_text_tokens=[]
	i=0
	for row in rows_text:
	 	rows_text_tokens.append(list(word for word in nltk.word_tokenize(row[0]) if word.isalpha()))
	 	print(rows_text_tokens[i])
	 	i+=1
	conn.close();
	

if __name__ == '__main__':
	main()
