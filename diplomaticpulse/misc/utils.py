"""
This module implements url parsing.
"""
from urllib.parse import unquote
import os
import langid
from scrapy.utils.project import get_project_settings


def get_language(text):
    """
    detect html content language.

    Args
        text (string):
            html text

    Returns
        language( string):
            content language

    Raises
        Exception
             when it catches  error

    """
    settings = get_project_settings()
    languages = settings["ARTICLES_LANGUAGE"]
    try:
        return languages[langid.classify(text)[0]]
    except Exception:
        return None


def get_url_extension(url):
    """
    extract url extension.

    Args
        url (string):
             link URL
    Returns
        extension (string)

    Raises
        Exception
             when it catches  error

    """
    try:
        return os.path.splitext(unquote(url))[1]
    except Exception:
        return None


def check_url(url):
    """
    check validity of an url.

    Args
        url (string):
            link URL

    Returns
        url (string)

    """
    try:
        url = unquote(url)
        url = url.replace(":443", "")  # Morocco url
        return url
    except Exception as ex:
        print(ex)
        return url
