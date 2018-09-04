import sqlite3
import numpy as np

def exec(conn,query):
	c=conn.cursor()
	c.execute(query)
	res=c.fetchall()
	c.close()
	return res

def main():
	conn=sqlite3.connect('01/database.sqlite')
	query="""select name from sqlite_master where type = 'table';"""
	print(exec(conn,query))
	#It contatins 1 table called Reviews
	query="""select * from Reviews limit 5"""
	print(exec(conn,query))
	

if __name__ == '__main__':
	main()
