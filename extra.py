""" This Module contains functions that can be used with any of the parsers And are not site specific """

import os
import shutil


def MakeDir(name, path, DefaultPath=None):
    """
    Makes a directory and chdir's into it.
    :param name: Name of the folder to be created : Generally  the name of the chapter.
    :param path: It is the path of the new folder to be created.
    :param DefaultPath: The path of Main manga folder.
    :return: None.
    """

    if DefaultPath is not None:
        os.chdir(DefaultPath)

    try:
        os.mkdir(name)
    except FileExistsError:
        pass

    os.chdir(path)


def site(url, site_number=None):
    """ Returns the site which the url is of. """
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


def Guess(site, name):
    """ Guesses the url for a given manga series based on name. 
    Takes the manga name from input and generates the main page url. 
    :param site: The Site whose url is to be if constructed:
    :param name: The name of the manga series."""

    # Both mangapanda and mangaseeonline delimit the words in a manda name by '-'
    # Using this, we can try to guess.
    # Else a search is to be initiated.
    name = name.strip(" ")  # Remove leading and trailing whitespaces
    manga_name = name
    for ch in (' ', ':', '#', '+'):
        manga_name = name.replace(ch, "-")  # convert to "-" delimited format. Eg. the-gamer

    manga_name = manga_name.replace('/', "")

    if site is 1:  # mangapanda.com
        url = "http://mangapanda.com/{}".format(manga_name)
        return url
    elif site is 2:  # mangaseeonline.us
        url = "http://mangaseeonline.us/manga/{}".format(manga_name)
        return url
    else:
        pass
