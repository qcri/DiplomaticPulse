"""
This module implements a string dates parser
"""
import re
import datetime
from datetime import date
import w3lib.html
import dateutil.parser as dparser
import dateparser
from scrapy.utils.project import get_project_settings



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
    """
    return avoid_future_date(dateparser.parse(date_string).strftime("%Y-%m-%d"))


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
    """
    Function that parses a string date with US format

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

    date_string_format = None
    if len(date_string.split("#")) == 2:
        date_string_format = date_string.split("#")[1]
    dispatcher = {
        "MDY": date_with_MDY_format,
        "MMDDYYYY": date_with_MMDDYYYY_format,
        "YYYYDDMM": date_with_YYYYDDMM_format,
        "YYDDMM": date_with_YYDDMM_format,
        "MMDDYY": date_with_MMDDYY_format,
    }
    date_string = fire_me(dispatcher[date_string_format], date_string.split("#")[0])
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
    """
    parse a string date using user entry format  MMDDYYYY

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
    """
    parse a string date using user entry format  YYYYDDMM

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
    """
    parse a string date using user entry format  YYDDMM

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
    """
    parse a string date using user entry format MMDDYY

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
    """
    force to today date if it is future date +1 (i.e: Australia dates)

    Args
        date_string : string
            string date

    Returns
        string date
    """

    try:
        st_date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        if st_date.date() > (date.today() + datetime.timedelta(days=1)):
            st_date =  date.today().strftime("%Y-%m-%d")
        else:
            st_date =  st_date.date().strftime("%Y-%m-%d")

        return st_date
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
        settings = get_project_settings()
        reg_exp_2 = settings["REG_EXP_2"]
        reg_st = re.search(reg_exp_2, st_date).group()
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
        posted_date = posted_date_in_raw["posted_date"]
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
