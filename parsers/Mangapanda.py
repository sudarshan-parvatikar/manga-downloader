# Following comments are for demo purposes only

## Make sure that the url from md.py never ends with "/"

# Eg Url : http://mangapanda.com/"manga_name"


import re
import urllib.request

try:
    from Model import Model
except:
    from .Model import Model

# Need to build opener

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)


class Mangapanda(Model):
    """ Parser for http://mangapanda.com/"""

    # counter = 0
    def __init__(self, url, start=1, stop=None):  # Initialises data
        self.name = self  # Examples here:
        self.url = url  # http://mangapanda.com/naruto
        self.start = start  # 1
        self.stop = stop  # 3

    def TotalPgs(self, chapter):
        """
        :param url: Url of the manga series. 
        :param no: Chapter to be parsed.
        :return: The total pages of the given manga chapter.
        """
        url = self.url + "/" + str(chapter)
        urlMP = url + '/1'  # http://mangapanda.com/naruto/4/1 ; url = http://mangapanda.com/naruto/4 + "/1"
        TotalPgsHtml = urllib.request.urlopen(urlMP).read().decode('utf-8')  # gets html for above url
        regexMP = re.compile(r'\d{1,3}(?=</div>)')
        TotalPgs = int(re.search(regexMP, TotalPgsHtml).group(0))  # Gets total pages
        return TotalPgs

    def GetSrc(self, url):
        """ Gets the src url of manga image of given page. """
        html_src = urllib.request.urlopen(url).read().decode('utf-8')  # Gets html from "url" in plain txt
        regexSrc = re.compile(r'(?<=src=").*[^"]\.(jpg|png)(?=" alt)')
        src = re.search(regexSrc, html_src).group(0)
        return src

    def imgGetter(self, imgurl, number):
        """This Function downloads the image in .jpg format. """
        imgName = str(number) + '.jpg'  # Choice for .png to be added
        urllib.request.urlretrieve(imgurl, imgName)

    def GetMangaName(self):
        """ This Function returns the name of the Manga of the given url. """
        MangaNameRegex = re.compile(r'(?<="aname">)\w{1,}(?=</h)')
        MangaNameHtml = urllib.request.urlopen(self.url).read().decode('utf-8')
        self.Main_Html = MangaNameHtml
        MangaName = re.search(MangaNameRegex, MangaNameHtml).group(0)
        return MangaName

    def CurrentUrl(self, chapter, number):
        """ This Function returns the url of a page of the current chapter. """
        currentUrl = self.url + '/' + str(chapter) + '/' + str(
            number)  # http://mangapanda.com/naruto + / + 1 + / + number(eg.1)
        return currentUrl

    def TotalChapters(self):
        """ Returns the Total Chapters of the given manga series. """
        Total_List = re.findall(r'(?<=\d">)\w.*\s\d{1,}(?=</a>)(?!.*</li>)', self.Main_Html)
        Total = re.search(r'\d{1,}', str(Total_List[-1])).group(0)
        Total_Chapters = int(Total)
        return Total_Chapters

    def GetCoverImage(self):
        """ Gets the cover image on the Main Manga page. """
        image_url = re.search(r'(?<=img\ssrc=").*\.(jpg|png)(?="\salt=")', self.Main_Html).group(0)
        urllib.request.urlretrieve(image_url, 'Cover Image.jpg')
        print("Got Cover Image.")
