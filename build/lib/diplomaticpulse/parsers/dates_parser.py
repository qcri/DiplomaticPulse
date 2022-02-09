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
    call function based on func_name

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
    parse a string date and handles multiple formats

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
    parse a non englisg string date.
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
    parse a non englisg string date.
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
    """parse a string date using user entry format  Feb032022

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
    """parse a string date using user entry format  MM-DD-YYYY

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
    """parse a string date using user entry format  YYYY-DD-MM

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
    """parse a string date using user entry format  YY-DD-MM

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
            dparser.parse(
                date_string, fuzzy=True, dayfirst=False, yearfirst=True
            ).strftime("%Y-%m-%d")
        )
    except Exception:
        return None


def date_with_MMDDYY_format(date_string):
    """parse a string date using user entry format MM-DD-YY

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
    if posted_date is not  None:
        return posted_date

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


if __name__ == "__main__":
    dates_english = [
        "2022/02/08",
        "2020/12/01",
        "12.10.2020  16:36",
        "01.10.2020  14:09",
        "09.07.2020",
        "2020.07.09",
        "1.3.2020",
        "2020.3.1",
        "2020/10/02",
        "02/10/2020",
        "17-09-11",
        "Feb032022#MDY",
        "09/24/2021#MMDDYYYY",
        "2018/03/10#YYYYDDMM",
        "17-09-11#YYDDMM",
        "11-09-11#MMDDYY",
        "Thursday, 20. August 2020",
        "Friday, 4th September 2020",
        "Monday, 9th November 2020",
        "1 July 2020 - 17:40",
        "Publication: 30-06-2020",
        "July 6, 2020",
        "Nov 17, 2020",
        "Press release, 09/07.2020",
        "4th March 2020",
        "Thursday, March 16, 2017",
        "July 10, 2020",
        "04 July 2020",
        "Date: 15/06/2020",
        "Date: 2020/11/05",
        "Date: 10/07/2020",
        "Date: 15/06/2020",
        "Date: 2020/06/02",
        "Publication: 15/06/2020",
        "Publication: 2020/11/05",
        "Publication: 10/07/2020",
        "Publication: 15/06/2020",
        "Date: 2020/06/02",
        "\r\n\t\tLast updated: \r\n\t\t10/25/2021 3:21 PM#MMDDYYYY",
        "Published: 04/06/18 01:35:00 pm",
        "05 Outubro de 2021  08h10",
        "12:41 / 10.09.2021",
        "12:41 / 10.09.2021",
        '<p><a href="pr091016.pdf">Federated States of Micronesia Establishes Diplomatic Ties with the United Arab Emirates</a> (9/10/16)</p>',
        '<p><a href="pubheal13.pdf">Public Service Announcement on Applying for the Pandemic Unemployment Assistance Program</a>, Palikir, June 17, 2020</p>',
        "Statement by the Minister of Foreign Affairs of the Republic of Belarus, Vladimir Makei, at the OSCE 26th Ministerial Council (Bratislava, December 5, 2019)",
        "Statement by the Press-Service of the Ministry of Foreign Affairs of the Republic of Belarus regarding terrorist attack in Istanbul (January 1, 2017, Minsk)",
        "vCentral design  23/02/15 committee session Tuesday 10/04 6:30 pm",
        "HIS MAJESTY THE SULTAN",
        "Ambassador Kelly Craft Permanent Representative U.S. Mission to the United Nations New York, New York June 25, 2020",
        "Statement by Minister of Foreign Affairs of Belarus V.Makei at the 24th Meeting of the OSCE Ministerial Council (December 7, 2017, Vienna)",
        "EU-Albania Stabilisation and Association Agreement 12th SUBCOMMITTEE ON JUSTICE, FREEDOM AND SECURITY 30 June-1 July 2020",
        "video conference 26 June 2020",
        "1 October 2020  MESSAGE OF CONDOLENCE TO HIS HIGHNESS THE AMIR OF THE STATE OF KUWAIT ON THE RECENT PASSING OF HIS HIGHNESS",
        "Statement by the Minister of Foreign Affairs of Belarus V.Makei at the General debate of the 74th session of the UN General Assembly (September 26 2019 New York)",
        "Statement of the Ministry for Europe and Foreign Affairs of the Republic of Albania Tirana 28.10.2020",
        "20201116121703",
        "Statement by the Minister of Foreign Affairs of the Republic of Belarus, Vladimir Makei, at the OSCE 26th Ministerial Council (Bratislava, December 5, 2019) Source: https://mfa.gov.by/en/press/statements/dad9272a52869cef.html © When using the site materials reference to the source is required",
        "Statement by Minister of Foreign Affairs of Belarus V.Makei at the 24th Meeting of the OSCE Ministerial Council (December 7, 2017, Vienna) Source: https://mfa.gov.by/en/press/statements/bc657b1107ac8f22.html © When using the site materials reference to the source is required.",
        "04 ????? ?????? 2020",
    ]

    dates_non_english = [
        "Mardi 01 Décembre 2020",
        "MERCREDI 27 MAI 2020",
        "3 mai, 2015",
        "mai  3 2015",
        "3 mayo, 2015",
        "Mayo 4, 2018",
        "AOut 4 2019",
        "12-Mayo-2019",
        " el 13 de julio, 2020",
        "sam 14/07/2018 - 12:00",
         "09 كانون الثاني 2022",
    ]

    # dates=[{'language':"Russian",'dt':'09.01.2022'}]
    # dates=[{'language':"Russian",'dt':'09.01.2022'},{'language':"Arabic",'dt':'09 كانون الثاني 2022'}]

    for st_dt in dates_english:
        print(st_dt, "-------", parse_mydate(st_dt, "english"))
    # # print("=================== no english")
    for st_dt in dates_non_english:
        print(st_dt, "-------", parse_mydate(st_dt, None))

    # get_date_from_pdf(posted_date, posted_date_in_raw, text, title):
    print(get_date_from_pdf(None, None, None, "this is my date 2020-05-04"))
