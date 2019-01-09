#!/usr/bin/python

""" Off-chain content filter database initialization """

import sqlite3, csv

def main():
    conn = sqlite3.connect('imageHashList.db')
    c = conn.cursor()
    # Create new table inside database with hashVal and fileName columns
    c.execute('''CREATE TABLE hashlist (hashVal varchar, fileName text)''')
    # Populate database from CSV file
    with open('hashlistMD5.csv','r') as file:
        dr = csv.DictReader(file)
        copyToDb = [(i['hashVal'], i['fileName']) for i in dr]
    c.executemany('INSERT INTO hashlist (hashVal, fileName) VALUES (?, ?);', copyToDb)
    
    #for row in c.execute('SELECT * FROM hashlist ORDER BY fileName'):
    #    print (row)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()

