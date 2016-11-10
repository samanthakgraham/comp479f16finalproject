from HTMLParser import HTMLParser
import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup
import argparse # Load argparse for command-line arguments

# We are going to create a class called LinkParser that inherits some
# methods from HTMLParser which is why it is passed into the definition
class LinkParser(HTMLParser):

	# This is a function that HTMLParser normally has
	# but we are adding some functionality to it
	def handle_starttag(self, tag, attrs):
		# We are looking for the begining of a link. Links normally look
		# like <a href="www.someurl.com"></a>
		if tag is 'a':
			for (key, value) in attrs:
				if key is 'href':
					# We are grabbing the new URL. We are also adding the
					# base URL to it. For example:
					# www.netinstructions.com is the base and
					# somepage.html is the new URL (a relative URL)
					#
					# We combine a relative URL with the base URL to create
					# an absolute URL like:
					# www.netinstructions.com/somepage.html
					newUrl = parse.urljoin(self.baseUrl, value)
					# And add it to our colection of links:
					self.links = self.links + [newUrl]

	# This is a new function that we are creating to get links
	# that our spider() function will call
	def getLinks(self, url):
		self.links = []
		# Remember the base URL which will be important when creating
		# absolute URLs
		self.baseUrl = url
		# Use the urlopen function from the standard Python 3 library
		response = urllib2.urlopen(url)

		# Make sure that we are looking at HTML and not other things that
		# are floating around on the internet (such as
		# JavaScript files, CSS, or .PDFs for example)
		pageSoup = BeautifulSoup(response, "html.parser")

		aTags = pageSoup.find_all('a')

		for tag in aTags:
			self.links.append(tag.get('href'))

		mainContent = pageSoup.find(id='content-main')		
		print mainContent
		divs = mainContent.find_all('div')
		pageText = ""
		for div in divs:
			pageText = pageText + div.get_text() + "\r\n"
		#print pageText.strip()

		if 'Content-Type: text/html' in response.info():
			htmlBytes = response.read()
			# Note that feed() handles Strings well, but not bytes
			# (A change from Python 2.x to Python 3.x)
			htmlString = htmlBytes.decode("utf-8")				
			self.feed(htmlString)
			return htmlString, self.links
		else:
			return "",[]	

# And finally here is our spider. It takes in an URL, a word to find,
# and the number of pages to search through before giving up
def spider(url, word, maxPages):  
	pagesToVisit = [url]
	numberVisited = 0
	foundWord = False
	# The main loop. Create a LinkParser and get all the links on the page.
	# Also search the page for the word or string
	# In our getLinks function we return the web page
	# (this is useful for searching for the word)
	# and we return a set of links from that web page
	# (this is useful for where to go next)
	while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
		numberVisited = numberVisited +1
		# Start from the beginning of our collection of pages to visit:
		url = pagesToVisit[0]
		pagesToVisit = pagesToVisit[1:]
		#try:
		print(numberVisited, "Visiting:", url)
		parser = LinkParser()
		data, links = parser.getLinks(url)

		if data.find(word)>-1:
			foundWord = True
			# Add the pages that we visited to the end of our collection
			# of pages to visit:
			pagesToVisit = pagesToVisit + links
			print(" **Success!**")
		#except:
		#	print(" **Failed!**")
	if foundWord:
		print("The word", word, "was found at", url)
	else:
		print("Word never found")

if __name__ == '__main__':
	# Create argument parser
	parser = argparse.ArgumentParser(description='This is the crawler for the COMP479 final project')

	# Add the arguments we'll accept
	parser.add_argument('-maxpages', metavar='max pages to visit', type=str, help='The maximum amount of child pages to visit for each url',default=5)

	# Get the argument(s) sent to us
	args = parser.parse_args()

	# List of urls we will scrape
	urlList = ["http://www.concordia.ca/artsci/biology.html", "http://www.concordia.ca/artsci/chemistry.html", "http://www.concordia.ca/artsci/exercise-science.html", "http://www.concordia.ca/artsci/geography-planning-environment.html", "http://www.concordia.ca/artsci/math-stats.html", "http://www.concordia.ca/artsci/physics.html", "http://www.concordia.ca/artsci/psychology.html", "http://www.concordia.ca/artsci/science-college.html"]
	spider(urlList[0], "buttsex", args.maxpages)
	#for url in urlList:
	#	spider(url, "buttsex", args.maxpages)











