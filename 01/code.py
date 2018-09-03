import sqlite3
import numpy as np


def main()
	conn=sqlite3.connect('01/database.sqlite')
	c=conn.cursor()
	query="""select name from sqlite_master where type = 'table';"""
	c.execute(query)
	print(c.fetchall())

if __name__ == '__main__':
	main()