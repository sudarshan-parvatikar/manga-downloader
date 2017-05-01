import argparse
import os
import urllib.request
from urllib.error import HTTPError
from urllib.request import urlopen

import extra
from parsers import Mangapanda, Mangasee

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

"""
A Multi Site Manga Downloader.
"""
__author__ = "Sudarshan Parvatikar"
__copyright__ = "Copyright 2017"
__credits__ = ["Sudarshan Parvatikar"]
__license__ = "MIT License, Tensai No License"
__version__ = "3.0"
__maintainer__ = "Sudarshan(Ashura)"
__email__ = "ashura@null.net"
__status__ = "Under Production"

print("\n\tMangaDownloader\n Author: {}\n Copyright: {}\n Credits: {}\n License: {}\n Version: {}\n".format(__author__, __copyright__, __credits__, __license__, __version__))

#######################################################################################################################################################################

parser = argparse.ArgumentParser(description="Command Line Mode.")

parser.add_argument("-u",
                    "--url",
                    help="Url of the manga to be downloaded.")

parser.add_argument("-b",
                    "--begin",
                    help="The chapter number to begin from or list of space seperated chapter numbers.")

parser.add_argument("-e",
                    "--end",
                    help="The chapter to end at."
                    )

parser.add_argument("-z",
                    "--zip",
                    action="store_true",
                    help="Enable if zipped chapters are needed.")

parser.add_argument("-i",
                    "--interactive",
                    action="store_true",
                    help="Enable if you want interactive Mode")

parser.add_argument("-a",
                    "--all",
                    action="store_true",
                    help="Download all the chapters")

parser.add_argument("-A",
                    "--Archive",
                    action="store_true",
                    help="Downloads All available chapters of the series, the cover Image and zips them")

parser.add_argument("-s",
                    "--site",
                    help="Enter 1 for mangapanda.com, 2 for mangaseeonline.us .")

parser.add_argument("-n",
                    "--name",
                    help="Enter the name of the manga series.")

args = parser.parse_args()

if args.interactive is True:
    """ For Interactive Mode. """
    args.url = None
    args.begin = None
    args.end = "int"
    args.zip = None

if args.all is True:
    """ In All Chapters Downloading mode."""
    args.begin = 1
    args.end = None  # None used to distinguish b/w interactive and all mode

if args.Archive is True:
    """ For Archive Mode. """
    args.all = True
    args.zip = True
    args.begin = 1
    args.end = "Archive"

if type(args.site) is str and type(args.name) is str:  # Guess the url of the manga series
    try:
        url = extra.Guess(int(args.site), args.name)  # get the guessed url
        x = urlopen(url)  # check if the url exists
        args.url = "Guessed"  # so that interactive mode doesn't gets implemented
    except HTTPError:  # if the url is wrong, go to interactive mode
        print("Guess didn't work, lets continue in interactive mode.")
        args.url = None

url = ""
total = 0
if args.url is None:
    url = str(input(
        "Enter the url of the manga.\n1)http://www.mangapanda.com/naruto : For mangapanda.com\n2)http://mangaseeonline.us/manga/naruto : For mangaseeonline.us \n"))
elif args.url is "Guessed":
    pass
else:
    url = args.url
    if url[-1] is "/":  # Remove trailing "/" if found
        url = url[0:-1]

if args.begin is None:
    start = int(input("Enter the chapter to start from.\n"))
else:
    start = int(args.begin)

if args.end is "int":  # "int" : Interactive, None : all chapters
    stop = input("Enter the chapter to stop at.\n")
    try:
        stop = int(stop)
        if stop == 0:
            stop = None
    except (ValueError, TypeError) as e:
        stop = None
elif args.end is None:
    stop = None
else:
    stop = args.end

zip_flag = ""  # Initialize zip_flag
if args.zip is None:  # interactive mode is enabled
    response = input(("Do you want zip archives of each chapter? Input 'y' for Yes ; 'n' for No.\n"))
    if response is 'y':
        zip_flag = True
    elif response is 'n':
        zip_flag = False
    else:
        zip_flag = False
elif args.zip is True:
    zip_flag = True

site = extra.site(url, int(args.site))


class InvalidSite(BaseException):  # Invalid Site Exception
    pass


class Error(BaseException):  # Other Errors Exception
    pass


## Lets Start downloading

if site is "Mangapanda":
    manga = Mangapanda.Mangapanda(url, start, stop)
    MangaName = manga.GetMangaName()
    Site = 1
elif site is "Mangasee":
    manga = Mangasee.Mangasee(url, start, stop)
    MangaName = manga.GetMangaName()
    Site = 2
else:
    raise InvalidSite("Error Site Not Supported.\nSee help.txt for more.!!!")

# The following logic was implemented due to non consistent naming of chapters by mangaseeonline.us
if args.end is "Archive":  # if -A is true, set stop = Total Chapters
    x = manga.TotalChapters()
    stop = len(x)
else:
    x = manga.TotalChapters()
    if Site is 1:
        stop = args.end
    elif Site is 2:
        if args.end is None:
            args.end = start
            int(args.end)
            stop = len(x[:args.end])

#################################################################################################################################################################

""" Main Logic For Downloading. """

if stop is None or start == stop:

    """ single chapter downloading mode """

    # MangaName = manga.GetMangaName()
    cwd = os.getcwd()
    NewPath = os.path.join(cwd, str(MangaName))
    extra.MakeDir(str(MangaName), NewPath)

    if args.Archive is True:  # Archive mode.
        manga.GetCoverImage()  # gets cover image under Archive Mode

    total = manga.TotalPgs(start)
    ChapterPath = os.path.join(NewPath, str(start))  # Creates a new path for chapter's folder
    extra.MakeDir(str(start), ChapterPath, NewPath)
    print("Chapter-{} is Starting!".format(start))
    for number in range(1, total + 1):
        currentUrl = manga.CurrentUrl(start, number)
        imgSrc = manga.GetSrc(currentUrl)
        manga.imgGetter(imgSrc, number)

    print("Chapter-{} is Downloaded".format(start))

    if zip_flag is True:  # Zipping of chapters.
        os.chdir('..')
        extra.zip(str(start), ChapterPath)
        print("Chapter-{} is Zipped!".format(start))
        extra.DeleteDir(ChapterPath)

else:
    """  Multi chapter Mode """

    # Making a New folder for MangaName
    cwd = os.getcwd()
    NewPath = os.path.join(cwd, str(MangaName))
    extra.MakeDir(str(MangaName), NewPath)

    if args.Archive is True:  # Archive mode
        manga.GetCoverImage()  # gets cover image under Archive Mode

    for i in range(start, stop + 1):  # i = Chapter Number(generally)
        if Site is 1:
            total = manga.TotalPgs(i)  # mangapanda is consistent in naming, so i is not altered
        elif Site is 2:
            total = manga.TotalPgs(int(x[i - 1]))  # mangaseeonline is non consistent, so i is changed
            x[i - 1] = i
        ChapterPath = os.path.join(NewPath, str(i))  # Creates a new path for chapter's folder
        extra.MakeDir(str(i), ChapterPath, NewPath)

        print("Chapter-{} is Starting!".format(i))

        for number in range(1, total + 1):  # number = page number
            currentUrl = manga.CurrentUrl(i, number)
            imgSrc = manga.GetSrc(currentUrl)
            manga.imgGetter(imgSrc, number)

        print("Chapter-{} is Downloaded".format(i))

        if zip_flag is True:  # zipping block
            os.chdir('..')
            extra.zip(str(i), ChapterPath)
            print("Chapter-{} is Zipped!".format(i))
            extra.DeleteDir(ChapterPath)

print("Download Complete!!!\n")
