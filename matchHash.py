#!/usr/bin/python

""" Off-chain content filter hash search program """

import sqlite3, hashlib

# queries the imageHashList.db for a signature match
def searchDB(imageHash):
    imageHash = imageHash.lower()
    conn = sqlite3.connect('imageHashList.db')
    c = conn.cursor()
    c.execute('SELECT rowid FROM hashlist WHERE hashVal = ?', (imageHash,))
    data = c.fetchone() 
    # if row exists, return positive match
    if data is not None:
        return True
    else: 
        return False

# produces MD5 hash of received data and calls searchDB()
def matchHashSig(data):
    imageHash = hashlib.md5(data).hexdigest()
    if (searchDB(imageHash)):
        return imageHash, True # match, return true and the hash value
    else:
        return False # if no match, return false
    
def main():
    pass # program is only called via main.py for the purpose of this work

if __name__ == '__main__':
    main()