"""
This module implements general some text parsing.
"""
import re
from urllib.parse import unquote
import os
import langid

from diplomaticpulse.dp_settings import read_settings

def get_language(text):
    """
    This method detects html content language. if language is unknown then it raises DropItem Exception.

    Args
        text (string):
            html text

    Returns
        language( string):

    Raises
        DropItem (Scrapy Exception)

    """

    try:
        languages = read_settings.get_languages()
        return languages[langid.classify(text)[0]]
    except TypeError:
        return None

def get_url_extension(url):
    """
    This method extracts extension of an URL.

    Args
        url (string):
             link URL
    Returns
        extension (string)

    Raises
        TypeError
             when it catches  error

    """
    try:
        return os.path.splitext(unquote(url))[1]
    except TypeError:
        return None


def to_reg_expression(text):
    """
    This method cleans string date using regular expression.

    Args
        text (string)

    Returns
       date (string)

    Raises
        Exception
             when it catches  error

    """
    try:
        reg_exp_2 = (
            "[0-9]{2}/[0-9]{2}/[0-9]{4}|[0-9]{2}.[0-9]{2}.[0-9]{4}|[0-9]{2}/[0-9]{2}/[0-9]{2}|[0-9]{1}/[0-9]{2}/[0-9]{2}|[0-9]{2}-[0-9]{2}-"
            "[0-9]{2}|[0-9]{4}.[0-9]{1}.[0-9]{1}|[0-9]{2}.[0-9]{1}.[0-9]{4}|[0-9]{4}.[0-9]{1}.[0-9]{1}|[0-9]{4}.[0-9]{2}.[0-9]{2}|[0-9]{1}."
            "[0-9]{1}.[0-9]{4}|[0-9]{1}.[0-9]{2}.[0-9]{4}|[0-9]{2}.[0-9]{2}.[0-9]{2}|[0-9]{2}.[0-9]{1}.[0-9]{2}|"
            r"(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2},"
            r" \d{4}|(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), \d{1,2}th (?:January|February|March|April|May|"
            r"June|July|August|September|October|November|December) "
            r"\d{4}|(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), \d{1,2}. (?:January|February|March|April|May|"
            r"June|July|August|September|October|November|December) \d{4}|\d{1,2} "
            r"(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}|(?:Jan|Feb|Mar|"
            r"April|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4}|\d{1,2}th "
            r"(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}|(?:January|"
            r"February|March|April|May|June|July|August|September|October|November|December) \d{1,2} \d{4}"
        )
        reg_st = re.search(reg_exp_2, text).group()
        return reg_st.replace("/", "-").replace(".", "-")
    except Exception:
        return text