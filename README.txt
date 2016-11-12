Final project for COMP479
Concordia University Fall 2016

Members:
Samantha Graham
Eric Watat Lowe
Constantino Mamani

This project uses the WebSphinx crawler to crawl a predefined set of links. These pages are then indexed for a sentiment analysis to be performed.

Usage:

1. Use WebSphinx GUI to crawl the URL's of your choice.
2. Run Lucene on the files the crawler returned using the following Windows cmd: java -classpath lucene-analyzers-common-6.3.0.jar;lucene-demo-6.3.0.jar;lucene-queryparser-6.3.0.jar;lucene-core-6.3.0.jar org.apache.lucene.demo.IndexFiles -docs path_to_files_dir
