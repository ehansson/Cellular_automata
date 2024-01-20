# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 03:02:16 2024

@author: ehansson
"""

def dec2binarylist(x):
    lst = []
    for i in range(8):
        r = x%2
        lst.insert(0, r)
        x = int((x-r)/2)
    return lst

def binarylist2dec(lst):
    x = 0
    for i in range(8):
        x += lst[i]*(2**(7-i))
    return x

def main():
    print(dec2binarylist(30), binarylist2dec([0, 0, 0, 0, 0, 1, 0, 1]))
    
if __name__=="__main__":
    main()