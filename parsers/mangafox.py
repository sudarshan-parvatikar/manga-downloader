""" I'm gonna implement this only if there's a problem with mangaseeonline.us """

# make sure that the url doesnt end with "/"

import re
import urllib.request

from Model import Model

# Need to build opener

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)


class Mangafox(Model):
    """ Parser for http://mangafox.me/"""
    counter = 0

    def __init__(self, url, start=1, stop=None, Manganame=None):  # Initialises data
        self.name = self  # Examples here:
        self.url = url  # http://mangafox.me/manga/naruto/
        self.start = start  # 1
        self.stop = stop  # 3

    def TotalPgs(self, url):
        urlMP = url + '/1'  # http://mangapanda.com/naruto/4/1 ; url = http://mangapanda.com/naruto/4 + "/1"
        TotalPgsHtml = urllib.request.urlopen(urlMP).read().decode('utf-8')  # gets html for above url
        regexMP = re.compile(r'\d{1,3}(?=</div>)')
        TotalPgs = int(re.search(regexMP, TotalPgsHtml).group(0))  # Gets total pages
        # print(TotalPgs)
        return TotalPgs
