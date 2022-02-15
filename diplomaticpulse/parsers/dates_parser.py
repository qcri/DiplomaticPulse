"""
This module implements a string dates parser
"""
import re
import datetime
import w3lib.html
from datetime import date
import dateutil.parser as dparser
import dateparser


exp_1 = (
    r"(?:\d{1,2} (?:january|february|march|april|may|june|july|august|september|october|november|december) \d{2,4})|(?:\d{1,2} "
    r"(?:jan|feb|march|april|may|june|july|august|sept|oct|nov|dec) \d{2,4})|(?:(?:january|february|march|april|may|june|july|"
    r"august|september|october|november|december)[,]? \d{1,2} \d{2,4})|"
    r"(?:(?:jan|feb|march|april|may|june|july|august|sept|oct|nov|dec)[,]? \d{1,2} \d{2,4})"
)

exp_2 = (
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


def fire_me(func_name, date_string):
    """
    Call function based on func_name.

    Args
        func_list (list of function to call):
                date_string : string date

    Returns
        text (string):
           string date
    """

    return func_name(date_string)


def parse_mydate(date_string, language):
    """
    Parse a string date and handles multiple formats.

    Args
        date_string  (string):
            string date to be parsed
        language (string):
            text language

    Returns
        date (string):
            parsed string date

    Raises
        Exception
             when it catches an error

    """
    func_ = "default"
    if len(date_string.split("#")) == 2:
        func_ = "date_with_US_format"
    elif language is None:
        func_ = "non_english"

    dispatcher = {
        "default": parse_default_date_string,
        "date_with_US_format": parse_date_with_US_format,
        "non_english": parse_non_english_date_string,
    }
    date_string = fire_me(dispatcher[func_], date_string)
    return date_string


def parse_non_english_date_string(date_string):
    """
    Parse a non englisg string date.
    eg: "Mardi 01 Décembre 2020"

    Args
        date_string  (string):
            string date to be parsed
        language (string):
            text language

    Returns
        date (string):
            parsed string date

    Raises
        Exception
             when it catches an error

    """
    try:
        return avoid_future_date(dateparser.parse(date_string).strftime("%Y-%m-%d"))
    except Exception:
        return None


def parse_default_date_string(date_string):
    """
    Parse a non englisg string date.
    eg: YYYY-MM-DD and DD-MM-YYYY

    Args
        date_string  (string):
            string date to be parsed
        language (string):
            text language

    Returns
        date (string):
            parsed string date

    Raises
        Exception
             when it catches an error

    """

    st_dt = None
    try:
        reg_st = to_reg_expression(date_string)
        st_dt = datetime.datetime.strptime(reg_st, "%d-%m-%Y").strftime("%Y-%m-%d")
    except Exception:
        st_dt = datetime.datetime.strptime(reg_st, "%Y-%m-%d").strftime("%Y-%m-%d")
        pass
    finally:
        if st_dt is None:
            try:
                st_dt = dparser.parse(
                    reg_st, fuzzy=True, dayfirst=True, yearfirst=False
                ).strftime("%Y-%m-%d")
            except Exception:
                pass
        return avoid_future_date(st_dt)


def parse_date_with_US_format(date_string):
    format = None
    if len(date_string.split("#")) == 2:
        format = date_string.split("#")[1]
    dispatcher = {
        "MDY": date_with_MDY_format,
        "MMDDYYYY": date_with_MMDDYYYY_format,
        "YYYYDDMM": date_with_YYYYDDMM_format,
        "YYDDMM": date_with_YYDDMM_format,
        "MMDDYY": date_with_MMDDYY_format,
    }
    date_string = fire_me(dispatcher[format], date_string.split("#")[0])
    return date_string


def date_with_MDY_format(date_string):
    """
    Function that parses a string date using specific entry format  Feb032022

    Args
        date_string : string
            string date

    Returns
        date: string
            parsed string date according to the format
    Raises
        Exception
             when it catches  error
    """
    try:
        res = datetime.datetime.strptime(date_string, "%b%d%Y").strftime("%Y-%m-%d")
        return avoid_future_date(res)
    except Exception:
        return None


def date_with_MMDDYYYY_format(date_string):
    """parse a string date using user entry format  MMDDYYYY

    Args
        date_string : string
            string date

    Returns
        date: string
            parsed string date according to the format
    Raises
        Exception
             when it catches  error
    """
    try:
        return avoid_future_date(
            dparser.parse(date_string, fuzzy=True, dayfirst=False).strftime("%Y-%m-%d")
        )
    except Exception:
        return None


def date_with_YYYYDDMM_format(date_string):
    """parse a string date using user entry format  YYYYDDMM

    Args
        date_string : string
            string date

    Returns
        date: string
            parsed string date according to the format
    Raises
        Exception
             when it catches  error

    """
    try:
        return avoid_future_date(
            dparser.parse(date_string, fuzzy=True, dayfirst=True).strftime("%Y-%m-%d")
        )
    except Exception:
        return None


def date_with_YYDDMM_format(date_string):
    """parse a string date using user entry format  YYDDMM

    Args
        date_string : string
            string date

    Returns
        date: string
            parsed string date according to the format
    Raises
        Exception
             when it catches  error

    """
    try:
        # convert it first to YYYYDDMM
        date_string = datetime.datetime.strptime(date_string, "%y-%d-%m").strftime(
            "%Y-%m-%d"
        )
        return date_with_YYYYDDMM_format(date_string)
    except Exception as ex:
        print("ERROR: ", ex)
        return None


def date_with_MMDDYY_format(date_string):
    """parse a string date using user entry format MMDDYY

    Args
        date_string : string
            string date

    Returns
        date: string
            parsed string date according to the format
    Raises
        Exception
             when it catches an error

    """
    try:
        return avoid_future_date(
            dparser.parse(
                date_string, fuzzy=True, dayfirst=False, yearfirst=False
            ).strftime("%Y-%m-%d")
        )
    except Exception:
        return None


def avoid_future_date(date_string):
    """force to today date if it is future date +1 (i.e: Australia dates)

    Args
        date_string : string
            string date

    Returns
        string date
    """

    try:
        dt_s = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        if dt_s.date() > (date.today() + datetime.timedelta(days=1)):
            return date.today().strftime("%Y-%m-%d")
        else:
            return dt_s.date().strftime("%Y-%m-%d")
    except Exception:
        return date.today().strftime("%Y-%m-%d")


def to_reg_expression(st_date):
    """clean date using to regular expression

    Args
        st_date : string
            dates

    Returns
        string date

    Raises
        Exception
             when it catches  error

    """
    try:
        reg_st = re.search(exp_2, st_date).group()
        return reg_st.replace("/", "-").replace(".", "-")
    except Exception:
        return st_date


def get_date(data, response, xpaths):
    """read article publised date

    Args
            title: string
                    article title
            response : Request response
                      response content
            xpaths : dict(json)
                    Python dict in the following format:
                    xpaths{
                        'title' : <article  title XPATH >
                    }

    Returns
            date : string
                article date

    Raises
        Exception
             when it catches  error

    """
    # try from response content
    st_date = (
        data["posted_date"]
        if data["posted_date"]
        else response.xpath(xpaths["posted_date"]).get()
    )
    # try from tile
    if st_date is None:
        st_date = parse_default_date_string(data["title"])

    # does it have US-Format
    try:
        if xpaths["us_date_format"]:
            st_date = st_date + "#" + xpaths["us_date_format"]
    except Exception:
        pass
    return st_date


def get_date_from_pdf(posted_date, posted_date_in_raw, text, title):
    """
    read published articledate

    Args
            data dict(json):
                    Python dict in the following format:
                    data{
                        'posted_date' : <article  posted_date >
                    }

    Returns
            date (string):
                article date

    Raises
        Exception
             when it catches  error

    """
    if posted_date is not None:
        return parse_default_date_string(posted_date)
    try:
        posted_date = posted_date_in_raw
    except Exception:
        pass

    if posted_date is None and title is not None:
        # try date from raw title
        try:
            posted_date = parse_default_date_string(title)
        except Exception:
            pass

    if posted_date is None and text is not None:
        # try date from statement body
        try:
            st = w3lib.html.remove_tags(text).replace("\r\n", "")
            posted_date = parse_default_date_string(st[-100:])
        except Exception:
            pass

    if posted_date is None:
        # use today's date
        posted_date = (datetime.datetime.now()).strftime("%Y-%m-%d")

    return posted_date

