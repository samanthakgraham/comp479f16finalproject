# Project 3 Indexer
# Author: Samantha Graham

from bs4 import BeautifulSoup # Load BeautifulSoup, for parsing HTML
import nltk # Load NLTK, for tokenizing
import string # Import string for some useful things
import os # Import the os module, for the os.walk function

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

# Main method
if __name__ == '__main__':    
  
    # Directory to crawl
    rootDir = './crawled_pages'

    # Get stopwords
    stopWords = importStopwords()
    
    # Instantiate the list of tokens
    tokenList = []

    # Keep track of the docIds
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
                    if word not in string.punctuation and "//www.concordia.ca" not in word and len(word) != 0 and word not in stopWords and word != 'http' and word.isalpha():
                        # And put the word in our list of tokens
                        tokenList.append([word.encode('ascii', 'ignore'), docId])

    # Now create the index
    index = {}

    for token, docId in tokenList:
        if token not in index:
            index[token] = {docId: 1}
        else:
            if docId not in index[token]:
                index[token].update({docId: 1})
            else:
                index[token][docId] = index[token][docId] + 1

    print index
    print len(index['oral'])







