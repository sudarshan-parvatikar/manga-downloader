# Parser for http://mangaseeonline.us/

# Make sure that the url from md.py never ends with "/"

# Eg. http://mangaseeonline.us/manga/"manga_name"

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

class InternalError(BaseException):
    pass

class Mangasee(Model):
    """ Parser for http://mangaseeonline.us/ """

    def __init__(self, url, start=1, stop=None):  # Initialises data
        # Examples here:
        self.url = url  # http://mangaseeonline.us/naruto
        self.start = start  # 1
        self.stop = stop  # 3
        self.link = self.url[31:]
        self.Total_Chapters = 0

    def TotalPgs(self, chapter):
        """
        Returns the number of pages of a manga chapter.
        
        :param no: Chapter to be parsed.
        :return: The total pages of the given manga chapter.
        """
        urlTP = "http://mangaseeonline.us/read-online/{}-chapter-{}-page-1".format(self.link,
                                                                                   chapter)  # http://mangaseeonline.us/read-online/Naruto-chapter-1-page-1.html
        TotalPgsHtml = urllib.request.urlopen(urlTP).read().decode('utf-8')  # gets html for above url
        regexMP = re.compile(r'(?<=Page\s)\d{1,3}(?=</option></select>)')
        TotalPgs = re.search(regexMP, TotalPgsHtml).group(0)
        return int(TotalPgs)

    def GetSrc(self, url):
        """
        Gets src url of image of input url(Pg.no).
        :param url: Url of Page to be parsed.
        :return: The url of img of given page.
        """
        html_src = urllib.request.urlopen(url)  # Gets html from "url"
        html_ = html_src.read().decode('utf-8')  # Plain text
        src = re.search(r'(?<=src=").*[^"]\.(jpg|png)(?=">)', html_).group(0)
        return src

    def GetMangaName(self):
        """ This Function returns the name of the Manga of the given url."""
        # global MangaName                                       # use TotalPgs()'s Html
        MangaNameRegex = re.compile(r'(?<=>)[\w-].*(?=</h1>)')
        MangaNameHtml = urllib.request.urlopen(self.url).read().decode('utf-8')
        self.Main_Html = MangaNameHtml
        MangaName = re.search(MangaNameRegex, MangaNameHtml).group(0)
        self.MangaName = MangaName
        return MangaName

    def imgGetter(self, imgurl, num, type=".jpg"):
        """This Function downloads the image in .jpg format. """
        imgName = str(num) + type  # Choice for .png to be added, Default .jpg
        urllib.request.urlretrieve(imgurl, imgName)

    def CurrentUrl(self, Chapter, number, url=""):
        """ This Function returns the url of a page of the current chapter. """
        # url is in the form of http://mangaseeonline.us/manga/"manga_name"
        # to avoid confusion, lets construct the url with the help of self.GetMangaName() Fn
        currentUrl = "http://mangaseeonline.us/read-online/{}-chapter-{}-page-{}.html".format(self.link, Chapter,
                                                                                              number)  # http://mangaseeonline.us/read-online/Naruto-chapter-"Chapter Number"-page-"Page Number".html
        # print(currentUrl)
        return currentUrl

    def TotalChapters(self):  # Always call this fn after GetMangaName
        self.Total_Chapters = []

        if len(self.Total_Chapters) is 0:
            TotalChapRegex = re.compile(r'(?<="chapterLabel">Chapter\s)(\d+(\.\d*)?)(?=</span)')  # for '"chapterLabel">Chapter ' Format
            Total_Chapters = re.findall(TotalChapRegex, self.Main_Html)  # Total_Chapters s in reversed format
            Total_Chapters = Total_Chapters[::-1]  # Reversing Total_Chapters
            self.Total_Chapters = list(dict(Total_Chapters).keys())

        elif len(self.Total_Chapters) is 1:  # the value is ['']
            TotalChapRegex = re.compile(r'(?<="chapterLabel">(root\.)\s)(\d+(\.\d*)?)(?=</span)')  # for '"chapterLabel">root. ' Format
            Total_Chapters = re.findall(TotalChapRegex, self.Main_Html)
            Total_Chapters = Total_Chapters[::-1]  # Reversing Total_Chapters
            self.Total_Chapters = list(dict(Total_Chapters).keys())

        elif len(self.Total_Chapters) is 1:
            TotalChapRegex = re.compile(r'(?<="chapterLabel">#\s)(\d+(\.\d*)?)(?=</span)')  # for '"chapterLabel"># ' Format
            Total_Chapters = re.findall(TotalChapRegex, self.Main_Html)
            Total_Chapters = Total_Chapters[::-1]  # Reversing Total_Chapters
            self.Total_Chapters = list(dict(Total_Chapters).keys())
        else:
            raise InternalError(" An internal problem has occured,"
                        " please notify the maintainer and use other site(s) till its fixed.\n"
                        "Error: mangasee-Total-Chapters.")


        # Total_Chapters = Total_Chapters[::-1]
        # self.Total_Chapters = list(dict(Total_Chapters).keys())
        return self.Total_Chapters

    def GetCoverImage(self):
        """ Gets the cover image on the Main Manga page. """
        image_url = re.search(r'(?<=img\ssrc=")(http://static\.mangaboss\.net).*\.(jpg|png)', self.Main_Html).group(0)
        urllib.request.urlretrieve(image_url, 'Cover Image.jpg')
        print("Got Cover Image.")
