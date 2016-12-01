# Project 3 Analyser
# Author: Constantino Mamani
from master.afinn import Afinn# Load Afinn
afinn = Afinn()# Initialize Afinn
from bs4 import BeautifulSoup # Load BeautifulSoup, for parsing HTML
import nltk # Load NLTK, for tokenizing
import string # Import string for some useful things
import os # Import the os module, for the os.walk function
from math import log10 # We need log for idf
import re # import regex expression

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
	
    termsPerPage = 0;
    termsPerDepartement = 0
	
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
			
			# Keep track of the the total score for each page
            termsPerPage = 0
		
            # Get all the paragraphs
            for paragraph in fileSoup.find_all('p'):
                #if fullFileName in (dirName + '/biology.html'):
                    paragraph = paragraph.get_text()
                    scorePerPage = scorePerPage + afinn.score(paragraph)
                    #print afinn.score(paragraph)
                    #print paragraph 
                    termsPerPage = termsPerPage + len(re.findall(r'\w+', paragraph))	
					
            pageList.append([fullFileName, scorePerPage])	
            print ("ScorePerPage: " + str(scorePerPage))
            scorePerLevel = scorePerLevel + scorePerPage
            termsPerDepartement = termsPerDepartement + termsPerPage
        
        if depth == 1:#means we went already through all the subdirectories since we start from bottom-up
            scorePerDepartment = scorePerDepartment + scorePerLevel;
            normalizedScorePerDep = scorePerDepartment/termsPerDepartement*100 	# score divided by the number of terms in the departement (multiply by 100 only to make score readable)
            departmentList.append([dirName, normalizedScorePerDep])
            print ("-------------------------------------------------ScorePerDepartement: (" + dirName + ") " + str(scorePerDepartment))
            print ("-------------------------------------------------NormalizedScorePerDepartement: (" + dirName + ") " + str(normalizedScorePerDep))
            scorePerLevel = 0
            scorePerDepartment = 0
            termsPerDepartement = 0
		
    for department, score in departmentList:
        print ("Department: " + department + " Score: " + str(score) + "")
	





