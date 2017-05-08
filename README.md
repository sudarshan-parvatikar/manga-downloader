# README #

A Program to download Webtoons.

### What is this repository for? ###

This program supports the following sites.  
* 1) http://mangapanda.com  
* 2) http://mangaseeonline.us  

### Requirements ###
* Python 3.x
* Tad bit of patience.

### Help ###
Usage:

 1) Command line mode.  
   Start cmd. Goto Main folder. Run:  
  	 > python md.py [arguments]  

Arguments:
	* -u, --url : url of main manga page. Put it in double quotes.  
	* -b, --begin: Starting chapter number.  
	* -e, --end: Chapter to end downloading at.  
	* -z, --zip: To zip the downloaded chapters.  
	* -a, --all: Downloads all chapters of given series.  
	* -A, --Archive: Downloads All available chapters of the series, the
                        cover Image and zips them.  
	* -s, --site: 1 - mangapanda.com, 2 - mangaseeonline.us .(To be used along with --name)  
	* -n, --name: The name of the manga series to be downloader.(Should be space delimited.)  
        * -g, --guess: Partial name of the series, the downloader tries to find a match. The Downloader will ask if displayed match is correct, if no match is selected, it exists.

* Note: Always use the following together:-
      1) -g and -s
      2) -n and -s

2) Interactive mode.   
  Start cmd. Goto Main folder. Run:  
      > python md.py -i  

Follow the on screen instructions.  

If any errors pop up, see Errors.txt .  

Happy Downloading.  
  
### Contribution guidelines ###

* Will see if project becomes large enough.

### Who do I talk to? ###

* ME! of course. ^_^