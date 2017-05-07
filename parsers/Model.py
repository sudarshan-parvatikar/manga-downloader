import abc


class Model(metaclass=abc.ABCMeta):
    """ Abstract Model Class for site parsers. """

    # Additional methods may be used depending on site.

    @abc.abstractmethod
    def __init__(self):
        """ Initialises variables such as url, start, stop, MangaName, with default values if needed. """
        return

    @abc.abstractmethod
    def GetSrc(self):
        """ Function used to get the src url of the image. """
        return

    @abc.abstractmethod
    def TotalPgs(self):
        """ Returns the total number of pages of the input Manga Chapter. """
        return

    @abc.abstractmethod
    def imgGetter(self):
        """ Downloads the image at given url. """
        return

    @abc.abstractmethod
    def GetMangaName(self):
        """ Returns  the Name of the given manga that is space delimited. """
        return

    @abc.abstractmethod
    def CurrentUrl(self):
        """ Returns the url of a page of the current chapter. """
        return

    @abc.abstractmethod
    def TotalChapters(self):
        """ Returns the total number of chapters of the given manga series."""
        return

    @abc.abstractmethod
    def GetCoverImage(self):
        """ Gets the Cover Image on the main manga page. """
        return

