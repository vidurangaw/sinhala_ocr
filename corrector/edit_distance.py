# -*- coding: utf-8 -*-
__author__ = 'AMali Rathnapriya'


import time
import sys
import  codecs
import os

package_directory = os.path.dirname(os.path.abspath(__file__))

DICTIONARY =('corrector/dictionary.txt')
# input_string=u"සංවිටාතමලිනුත් ඉල්ලා ග�තක් කො�ඹ දමස්ටාවලදී ඡලාගවලිත් තාලසත් පිලිසමත් පයළොස්මත නවයුකු නාමතාලිත මණ්ඩලය සංවිටාතයකින් යන්තද්ටව රඡමිහා ටිනාරය පයුතර නරමක්"
# input_string=input_string.split(' ')


# input_string= u"ජලාග විමල් ව සංමිධාතය"
# input_string=input_string.split(" ")
# MAX_COST =2

# Keep some interesting statistics
NodeCount = 0
WordCount = 0


class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}

        global NodeCount
        NodeCount += 1

    def insert( self, word ):
        node = self
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()

            node = node.children[letter]

        node.word = word

# read dictionary file into a trie
trie = TrieNode()
for word in codecs.open(DICTIONARY,encoding='utf-8').read().split():
    WordCount += 1
    trie.insert( word )

print "Read %d words into %d nodes" % (WordCount, NodeCount)


def search( word, maxCost ):

    # build first row
    currentRow = range( len(word) + 1 )

    results = []

    # recursively search each branch of the trie
    for letter in trie.children:
        searchRecursive( trie.children[letter], letter, word, currentRow,
            results, maxCost )

    return results


def searchRecursive( node, letter, word, previousRow, results, maxCost ):

    columns = len( word ) + 1
    currentRow = [ previousRow[0] + 1 ]


    for column in xrange( 1, columns ):

        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1

        if word[column - 1] != letter:
            replaceCost = previousRow[ column - 1 ] + 1
        else:
            replaceCost = previousRow[ column - 1 ]

        currentRow.append( min(replaceCost,insertCost,deleteCost) ) #can add insertCOst and deleteCost  as min( replaceCost, deleteCost, insertCost)


    if currentRow[-1] <= maxCost and node.word != None:
        results.append( node.word )

    # if any entries in the row are less than the maximum cost, then recursively search each branch of the trie
    if min( currentRow ) <= maxCost:
        for letter in node.children:
            searchRecursive( node.children[letter], letter, word, currentRow,
                results, maxCost )


def correct(input_string):
    # MAX_COST=0
    correction={}
    suggestion=[]
    start = time.time()

    # for item in input_string:
    item="".join(input_string)
    TARGET = item
    print "\n",(TARGET),"............"
    if item.__len__()==1 or item.__len__()==2:
                results = search( TARGET, 0 )
                if results is not None:
            # for result in results:
            #     suggestion='%s' % ''.join([''.join('%s' % ''.join(e) for e in results)])
                    suggestion=results
                # if suggestion!=None:
                    print (suggestion)
    elif item.__len__()==3 or item.__len__()==4:
                results=search(TARGET,1)
                if results is not None:
            # for result in results:
                    suggestion=results
            #     suggestion='%s' % ''.join([''.join('%s' % ''.join(e) for e in results)])
                # if suggestion!=None:
                    print (suggestion)
    elif item.__len__()==5:
            # results=search(TARGET,2)
                results=search(TARGET,2)
                if results !=[]:
            # for result in results:
                    suggestion=results
                else:
                    results=search(TARGET,4)
                    suggestion=results
            #     suggestion='%s' % ''.join([''.join('%s' % ''.join(e) for e in results)])
                # if suggestion!=None:
                    print (suggestion)
    elif item.__len__()==6:
                results=search(TARGET,2)
                if results is not None:
        # for result in results:
                    suggestion=results
        #         suggestion='%s' % ''.join([' '.join('%s' % ''.join(e) for e in results)])
                # if suggestion!=None:
                    print (suggestion)
    else:
                results=search(TARGET,3)
                if results is not None:
        # for result in results:
                    suggestion=results
        #         suggestion='%s' % ''.join([' '.join('%s' % ''.join(e) for e in results)])
                # if suggestion!=None:
                    print (suggestion)




    end = time.time()

    # results_final=[]
    # for item in results:
    #     if item!=None or item!="":
    #
    #         results_final=results_final.append(item)

    results=results[:4]
    correction=results
    print "Search took %g s" % (end - start)

    return correction



# correct(input_string)