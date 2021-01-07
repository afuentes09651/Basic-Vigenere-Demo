# Author:Armando Fuentes
# ULID: C00296127
# Course: CMPS 315
# Assignment: pa1 - Vigenere cipher
# I certify that this assignment is entirely my own work

from string import ascii_lowercase
from math import log10
from itertools import product
import collections
import os


def decrypt(ciphertext, key):
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    ciphertext_int = [ord(i) for i in ciphertext]
    plaintext = ''
    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
        plaintext += chr(value + 65)
    return plaintext


class ngram_score(object):
    def __init__(self,ngramfile,sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        file = open (ngramfile)
        for line in file: #(ngramfile):
            key,count = line.split(sep)
            self.ngrams[key] = int(count)
        self.L = len(key)

        #self.N = sum(self.ngrams.itervalues())
        self.N = sum(self.ngrams.values())

        #calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)
        self.floor = log10(0.01/self.N)

    def score(self,text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__

        #for i in xrange(len(text)-self.L+1):
        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams: score += ngrams(text[i:i+self.L])
            else: score += self.floor
        return score

def main():
    #open file
    with open('cipher.txt', 'r') as file:
        ciphertext = file.read().replace('\n', '')

    #frequency analysis
    key0 = ciphertext[0::3]
    key1 = ciphertext[1::3]
    key2 = ciphertext[2::3]

    #display frequency results


    keys0 = collections.Counter(key0).most_common(5)
    letters0 = []
    counts0 = []


    #Key 0
    for key in keys0:
        letters0.append(key[0])
        counts0.append(key[1])

    print('Top Values Key 0: ', end=' ')
    print(letters0)

    print('Top Counts Key 0: ',end=' ')
    print(counts0)

    #Key 1
    keys1 = collections.Counter(key1).most_common(5)
    letters1 = []
    counts1 = []

    for key in keys1:
        letters1.append(key[0])
        counts1.append(key[1])

    print('Top Values Key 1: ', end=' ')
    print(letters1)

    print('Top Counts Key 1: ',end=' ')
    print(counts1)

    #Key 2
    keys2 = collections.Counter(key2).most_common(5)
    letters2 = []
    counts2 = []

    for key in keys2:
        letters2.append(key[0])
        counts2.append(key[1])

    print('Top Values Key 2: ', end=' ')
    print(letters2)

    print('Top Counts Key 0: ',end=' ')
    print(counts2)

    print()

    #now lets get the shift amounts
    ct = 0

    while ct < 5:
        letters0[ct] = chr(((ord(letters0[ct]) - ord('e')) % 26) + 97)
        letters1[ct] = chr(((ord(letters1[ct]) - ord('e')) % 26) + 97)
        letters2[ct] = chr(((ord(letters2[ct]) - ord('e')) % 26) + 97)
        ct += 1

    keys = []

    #construct the possible keys
    for x in letters0:
        key = x
        for y in letters1:
            key += y
            for z in letters2:
                key += z
                keys.append(key)

    #decryption time
    ng = 9999 #dummy val for ngram to start off with
    curkey = ''
    curdec = ''
    keywords = (''.join(i) for i in keys) #some logic to get all possible keys
    for keyword in keywords:
        decoded = decrypt(ciphertext, keyword) #getting our decoded text
        currng = ngram_score('english_monograms.txt').score(decoded)
        #use this logic to determine the best key
        if(abs(currng) < abs(ng)):
            ng = currng
            curdec = decoded
            curkey = keyword
    #print results
    print('Best ngram score: ',end=' ')
    print(ng)
    print('Best key: ',end=' ')
    print(curkey)
    print('Recovered plaintext: ',end='\n\n')
    print(curdec)

if __name__ == '__main__':
    main()