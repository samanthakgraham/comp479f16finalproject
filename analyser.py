# Project 3 Indexer
# Author: Constantino Mamani
from master.afinn import Afinn# Load Afinn
afinn = Afinn()# Initialize Afinn
from bs4 import BeautifulSoup # Load BeautifulSoup, for parsing HTML
import nltk # Load NLTK, for tokenizing
import string # Import string for some useful things
import os # Import the os module, for the os.walk function
from math import log10 # We need log for idf

# Main method
if __name__ == '__main__':    
  
    # Directory to crawl
    rootDir = './crawled_pages'
    
    # Instantiate the list of pages
    pageList = []

    # Instantiate the list of department
    departmentList = []
	
    scorePerDepartment = 0;
    scorePerLevel = 0
	
    # Walk thru the crawled pages directory
    for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):#Traverse bottom-up
 	
        depth = len(dirName.replace(rootDir, "").split('\\')) - 1#directory depth, Windows Linux ??? "\" or "/"

        for fname in fileList:
            fullFileName = dirName + '/' + fname
            print fullFileName
			
			#Open the file into BeautifulSoup
            fileSoup = BeautifulSoup(open(fullFileName), "html.parser")
            fileSoup.a.decompose()
			
            # Keep track of the the total score for each page
            scorePerPage = 0
			
            # Get all the paragraphs
            for paragraph in fileSoup.find_all('p'):
                #if fullFileName in (dirName + '/biology.html'):
                    paragraph = paragraph.get_text()
                    scorePerPage = scorePerPage + afinn.score(paragraph)
                    print afinn.score(paragraph)
                    #print paragraph 
					
            pageList.append([fullFileName, scorePerPage])	
            print ("ScorePerPage: " + str(scorePerPage))
            scorePerLevel = scorePerLevel + scorePerPage
        
        if depth == 1:#means we went already through all the subdirectories since we start from bottom-up
            scorePerDepartment = scorePerDepartment + scorePerLevel;				
            departmentList.append([dirName, scorePerDepartment])
            print ("-------------------------------------------------ScorePerDepartement: (" + dirName + ") " + str(scorePerDepartment))
            scorePerLevel = 0
            scorePerDepartment = 0
		
    for department, score in departmentList:
        print ("Department: " + department + " Score: " + str(score) + "")
	