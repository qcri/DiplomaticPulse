"""
This module implements  string dates parsing codes.
"""
import datetime
from datetime import date
import w3lib.html
import dateutil.parser as dparser
import dateparser
from diplomaticpulse.misc import utils

def parse_mydate(index_action):
    """
    This function parses any string date.

    Args
        str_date (string):
            string date to be parsed
        language (string):
            text language, eg: english

    Returns
        date (string)

    """
    language = None
    if 'language' in index_action:
        language = index_action['language']
    str_date = None
    if 'posted_date' in index_action:
        str_date = index_action['posted_date']

    func_name = "default"
    if language is not None and language.lower() != 'english':
        func_name = "non_english"
    elif str_date is not None and  len(str_date.split("#")) > 1:
            func_name = "date_with_us_format"

    dispatcher = {
        "default": parse_default_string_date,
        "date_with_us_format": parse_date_with_US_format,
        "non_english": parse_non_english_string_date,
    }
    return fire_me(dispatcher[func_name], str_date)


def fire_me(func_name, str_date):
    """
    Call function is based on func_name.

    Args
        func_name (string:
             function name to call
        str_date (string):
             string fate

    Returns
           string date (string)
    """

    return avoid_future_date(func_name(str_date))

def parse_non_english_string_date(str_date):
    """
    This function parses a non english string date, eg: "Mardi 01 Décembre 2020".

    Args
        str_date  (string):
            string date to be parsed

    Returns
        date (string):
            parsed string date
    """
    try:
        return dateparser.parse(str_date).strftime("%Y-%m-%d")
    except Exception as ex:
        print(ex)
        return None


def parse_default_string_date(str_date):
    """
    This function parses string date, format: YYYYMMDD and DDMMYYYY.

    Args
        str_date  (string):
            string date to be parsed

    Returns
        date (string)

    Raises
        Exception
             when it catches an error

    """
    reg_st = utils.to_reg_expression(str_date)
    try:
        #check DD-MM-YYYY
        return (datetime.datetime.strptime(reg_st, "%d-%m-%Y").strftime("%Y-%m-%d"))
    except Exception:
        pass

    try:
        # check YYYY-MM-DD
        return datetime.datetime.strptime(reg_st, "%Y-%m-%d").strftime("%Y-%m-%d")
    except Exception:
        parsed_st_dt=None

    if parsed_st_dt is None:
        try:
            # scrapes date from text
            parsed_st_dt = dparser.parse(
                    reg_st, fuzzy=True, dayfirst=True, yearfirst=False
                ).strftime("%Y-%m-%d")
        except Exception:
            parsed_st_dt=None
    return parsed_st_dt


def parse_date_with_US_format(string_date):
    """
    This function parses string date , format: YYYYDDMM, MMDDYYYY

    Args
        string_date (string):
            string date

    Returns
        date(string)

    Raises
        ValueError
             when it catches  error
    """
    if len(string_date.split("#")) <2:
        return None

    str_date = string_date.split("#")[0]
    dt_format = string_date.split("#")[1]

    dispatcher = {
        "MDY": date_with_MDY_format,
        "MMDDYYYY": date_with_MMDDYYYY_format,
        "YYYYDDMM": date_with_YYYYDDMM_format,
        "YYDDMM": date_with_YYDDMM_format,
        "MMDDYY": date_with_MMDDYY_format,
    }
    return fire_me(dispatcher[dt_format], str_date)


def date_with_MDY_format(str_date):
    """
     This function parses a string date, format:  Feb032022

    Args
        str_date (string):
            string date

    Returns
        parsed date(string)

    Raises
        ValueError
             when it catches  error
    """
    try:
        return datetime.datetime.strptime(str_date, "%b%d%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None


def date_with_MMDDYYYY_format(str_date):
    """
    This method parses string date, format: MMDDYYYY

    Args
        str_date (string)
            string date

    Returns
        date (string)

    Raises
        Exception
             when it catches  error
    """
    try:
        return   dparser.parse(str_date, fuzzy=True, dayfirst=False).strftime("%Y-%m-%d")
    except Exception:
       return None

def date_with_YYYYDDMM_format(str_date):
    """
    This function parse a string date using user entry format: YYYYDDMM.

    Args
        str_date ( string)
            string date

    Returns
        date (string)
    Raises
        Exception
             when it catches  error

    """
    try:
        return   dparser.parse(str_date, fuzzy=True, dayfirst=True).strftime("%Y-%m-%d")
    except Exception:
        return None


def date_with_YYDDMM_format(str_date):
    """
    This method parses string date, format: YYDDMM.

    Args
        str_date (string)
            string date

    Returns
        date (string):

    Raises
        ValueError
             when it catches  error

    """
    try:
        # convert it first to YYYYDDMM
        str_date = datetime.datetime.strptime(str_date, "%y-%d-%m").strftime(
            "%Y-%m-%d"
        )
        return date_with_YYYYDDMM_format(str_date)
    except ValueError:
        return None


def date_with_MMDDYY_format(str_date):
    """
    This method parses string date, format:MMDDYY

    Args
        str_date (string):
            string date

    Returns
        date (string)

    Raises
        Exception
             when it catches an error

    """
    try:
        return   dparser.parse(
                str_date, fuzzy=True, dayfirst=False, yearfirst=False
            ).strftime("%Y-%m-%d")

    except Exception:
        return None


def avoid_future_date(str_date):
    """
    This method forces today's date if it is [future date +1] (i.e: Australia dates)

    Args
        str_date ( string):
            string date

    Returns
        date (string)

    """

    try:
        st_date = datetime.datetime.strptime(str_date, "%Y-%m-%d")
        if st_date.date() > (date.today() + datetime.timedelta(days=1)):
            st_date =  date.today().strftime("%Y-%m-%d")
        else:
            st_date =  st_date.date().strftime("%Y-%m-%d")

        return st_date
    except Exception:
        return date.today().strftime("%Y-%m-%d")


def get_date(data, response, xpaths):
    """
    This method scrapes date from text.

    Args
        data dict(json):
            Python dict in the following format:
            {
              "posted_date" : <posted_date>
            }
            response : Request response
                      response content
        xpaths  dict(json):
                    Python dict in the following format:
                    xpaths{
                        'title' : <article  title XPATH >
                    }

    Returns
            date (string)

    """

    str_date = None
    if data and 'posted_date' in data:
        str_date = data["posted_date"]

    if str_date is None and "posted_date" in xpaths:
        str_date = response.xpath(xpaths["posted_date"]).get()

    # try from text:tile
    if str_date is None and "title" in xpaths:
        str_date = parse_default_string_date(data["title"])

    # Concatenate US-Format to string date
    if str_date and  xpaths['us_date_format']:
        str_date = str_date + "#" + xpaths["us_date_format"]

    return str_date if str_date is not None  else avoid_future_date(str_date)


def get_date_from_pdf(str_date, posted_date_in_raw, text, title):
    """
    read published article date.

    Args
            data dict(json):
                    Python dict in the following format:
                    data{
                        'posted_date' : <article  posted_date >
                    }

    Returns
            date (string):

    Raises
        Exception
             when it catches  error

    """
    try:
        if str_date is not None:
            return parse_default_string_date(str_date)

        try:
            str_date = posted_date_in_raw["posted_date"]
        except Exception:
            pass

        if str_date is None and title is not None:
            # try date from raw title
            str_date = parse_default_string_date(title)

        if str_date is None and text is not None:
            # try date from statement body
            try:
                st = w3lib.html.remove_tags(text).replace("\r\n", "")
                str_date = parse_default_string_date(st[-100:])
            except Exception:
                pass

        if str_date is None:
            # use today's date
            str_date = (datetime.datetime.now()).strftime("%Y-%m-%d")

        return str_date

    except Exception:
        return None
