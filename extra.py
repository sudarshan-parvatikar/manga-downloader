""" This Module contains functions that can be used with any of the parsers And are not site specific """

import os
import shutil
import urllib.request
import re

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

def MakeDir(name, path, DefaultPath=None):
    """
    Makes a directory and chdir's into it.
    :param name: Name of the folder to be created : Generally  the name of the chapter.
    :param path: It is the path of the new folder to be created.
    :param DefaultPath: The path of Main manga folder.
    :return: None.
    """

    if DefaultPath is not None:
        try:
            os.chdir(DefaultPath)
        except:
            pass

    try:
        os.mkdir(name)
    except (FileExistsError):
        pass

    os.chdir(path)


def site(url, site_number=None):
    """ Returns the site which the url is of. """
    if site_number is not None:
        site_number = int(site_number)
    if "panda" in url or site_number is 1:
        return "Mangapanda"
    elif "mangasee" in url or site_number is 2:
        return "Mangasee"
    else:
        raise Exception("Site Not Supported. See Help / Readme.md for Supported sites.")


def zip(output_filename, dir_path):
    """ Zips the Directory, rest is self explanatory. """
    shutil.make_archive(output_filename, 'zip', dir_path)


def DeleteDir(path):
    """ Deletes the Directory at 'path'. """
    shutil.rmtree(path)


def Guess(website, name):
    """ Guesses the url for a given manga series based on name. 
    Takes the manga name from input and generates the main page url. 
    :param website: The Site whose url is to be if constructed.
    :param name: The name of the manga series."""

    # Both mangapanda and mangaseeonline delimit the words in a manda name by '-'
    # Using this, we can try to guess.
    # Else a search is to be initiated.
    name = name.strip(" ")  # Remove leading and trailing whitespaces
    manga_name = name.lower()       # covert into lowercase for easy use.
    for ch in (' ', '#', '+'):
        if ': ' in name:
            name = name.replace(':', "")
        elif ' -' or '- ' or ' - ' or ' : ' in name:
            for char in (' -', '- ', ' : '):
                name = name.replace(char, "-")
        manga_name = name.replace(ch, "-")  # convert to "-" delimited format. Eg. the-gamer
        name = manga_name


    manga_name = manga_name.replace('/', "")

    if int(website) is 1:  # mangapanda.com
        url = "http://mangapanda.com/{}".format(manga_name)
        return url
    elif int(website) is 2:  # mangaseeonline.us
        url = "http://mangaseeonline.us/manga/{}".format(manga_name)
        return url
    else:
        return None


def Search(manga_site, guess):
    """
    Searches the manga directory of the site to match the guess.
    :param guess: the name of the manga.
    :param manga_site: the site to be searched.
    :return: list containing matches.
    """
    series_re = re.compile(r'(?<=">).*(?=</a>)')
    if manga_site is 1:
        directory = urllib.request.urlopen("http://www.mangapanda.com/alphabetical").read().decode('utf-8')
    elif manga_site is 2:
        directory = urllib.request.urlopen("http://mangaseeonline.us/directory/").read().decode('utf-8')
    else:
        raise Exception("ERROR!!!\nRefer help.txt for more.")

    temp = re.findall(series_re, directory)
    match = []

    for text in temp:
        if guess in text.lower():
            match.append(text)
    return match

def Namer(name):
    """ Converts the input name to '-' delimited format."""
    name = name.strip(' ')
    name = name.replace(' : ', '-')
    for ch in (': ', ' :', '# ', '. ', '- ', ' ', '_', '#', '+',):
        name.strip(ch)
        name = name.replace(ch, '-')
    name = name.strip('-')                          # -naruto- isnt hot.
    name = name.replace('--', '-')                  # Boruto--Naruto isn't sexy.
    name = name.replace('---', '-')                 # Second pass

    return name

