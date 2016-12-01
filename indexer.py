# Project 3 Indexer
# Author: Samantha Graham

from bs4 import BeautifulSoup # Load BeautifulSoup, for parsing HTML
import nltk # Load NLTK, for tokenizing
import string # Import string for some useful things
import os # Import the os module, for the os.walk function
from math import log10 # We need log for idf
from collections import OrderedDict # To have an ordered dictionary

# "raw" index in the form { 'term' : { docId : term frequency in docId } }, for the first pass
rawIndex = {}

# The new, final index will be of the form { 'term' : { docId: tf-idf weight for this term in this docId } }
index = {}

# Imports the list of stopwords from a file and saves them in a list for future use
def importStopwords():
    # Instantiate list of stopwords
    stopWords = []
    
    # Open file
    stopFile = open('stopwords.txt', 'r')

    # Import stopwords from file into list
    for line in stopFile:
        stopWords.append(line.strip())

    return stopWords

# Function to sort a dictionary into an OrderedDict
def sortIndex(index):    
    # We'll save the new index as an OrderedDict to retain the order
    sortedIndex = OrderedDict()
        
    # Sort all the things
    sortedTerms = sorted(index)
    for term in sortedTerms:
        sortedIndex[term] = index[term]

    # Return
    return sortedIndex

# Main method
if __name__ == '__main__':    
  
    # Directory to crawl
    rootDir = './crawled_pages'

    # Get stopwords
    stopWords = importStopwords()
    
    # Instantiate the list of tokens
    tokenList = []

    # Keep track of the docIds; this is also the number of docs, N
    docId = 0

    # Walk thru the crawled pages directory
    for dirName, subdirList, fileList in os.walk(rootDir):        
        for fname in fileList:
            fullFileName = dirName + '/' + fname
            print fullFileName
            
            # Increment docId
            docId = docId + 1            
            
            #Open the file into BeautifulSoup
	    fileSoup = BeautifulSoup(open(fullFileName), "html.parser")
	    fileSoup.a.decompose()
	    
	    # Get all the paragraphs
	    for paragraph in fileSoup.find_all('p'):
                # Get the paragraph's text
                paragraph = paragraph.get_text()

                # Get all the tokens in the paragraph
                tokens = nltk.word_tokenize(paragraph.strip(string.punctuation))

                # Loop thru the tokens
                for word in tokens:
                    # Make the word lowercase
                    word = word.lower()

                    # Do a bunch of compression
                    if word not in string.punctuation and "//www.concordia.ca" not in word and len(word) > 2 and word not in stopWords and word != 'http' and word.isalpha():                        
                        # And put the word in our list of tokens
                        tokenList.append([word.encode('ascii', 'ignore'), docId])	

	# Save the number of documents in N to avoid confusion for later
	N = docId
    
    # Go thru all the tokens in the list
    for token, doc in tokenList:
        # If this token isn't in the index yet
        if token not in rawIndex:
            # Add it to the index
            rawIndex[token] = {doc: 1}
        else:
            # If this docId isn't in the postings list for this term
            if docId not in rawIndex[token]:
                # Add it to the postings list
                rawIndex[token].update({doc: 1})
            else:
                # Increment the term frequency for this term in this docId
                rawIndex[token][doc] = rawIndex[token][doc] + 1
    
	# Now, use the raw index to calculate tf-idf for each term in each document.	

	# Loop thru terms in rawIndex
	for term in rawIndex:
		# Save an entry for it in the final index
		index[term] = {}

		# Loop thru docIds for this term
		for doc in rawIndex[term]:
			# Get the term frequency, saved in the raw index
			termFreq = rawIndex[term][doc]

			# Get the document frequency, the length of the dict for this term
			docFreq = len(rawIndex[term])

			# Calculate the idf
			inverseDocFreq = (log10(N)) / docFreq
	
			# Calculate tf-idf for this term in this document
			tfIdf = termFreq * inverseDocFreq

			# And save it in the index
			index[term][doc] = tfIdf

    # Sort the index
    fullSortedDictionary = OrderedDict()
    fullSortedDictionary = sortIndex(index)
	
    # Move the index into one file for searching later
    indexFile = open('index.txt', 'wb')
    indexFile.write(str(fullSortedDictionary))






