"""
This module implements beautifulsoup object bs4 parsing
"""
from urllib.parse import unquote
import time
from bs4 import BeautifulSoup

from diplomaticpulse.parsers import dates_parser


def get_bs4_soup(url, driver):
    """
    Get Beautifulsoup soup object.

    Args
        url (string):
            link url
        driver (Selenium driver type):
            driver object

    Returns
        soup(object of beautifulsoup)

    """
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        return soup
    except Exception as e:
        print("Warming: failed to get Beatifulsoup object for ", e)
        return None


def remove_unwanted_tags(url, driver, xpaths):
    """
    Remove unwanted tags element from html content.

    Args
        url (string):link URL
        driver (Selenium driver): driver
        xpaths dict(string):unwanted elements names

    Returns
         text (string):
            cleaned html text

    """
    try:
        soup = get_bs4_soup(url, driver)
        elements = xpaths["tags"].split("#")
        for elem in elements:
            tags = elem.split(",")
            if len(tags) > 1:
                for tag in soup.find_all(tags[0], class_=tags[1]):
                    tag.extract()
            else:
                tags_to_delete = soup.find_all(elem)
                for tag in tags_to_delete:
                    tag.extract()
        return soup
    except Exception as e:
        print("WARNING in remove_unwanted_tags: ", str(e))
        return None


def get_bs4_data_from_blocks(response, xpaths, driver):
    """
    Scrape article  html block (as seen in page overview).

    Args
        response (response object):
           html content
        xpaths dict(json):
            xpaths {
                'global' : <page html block XPATH ofr each article>
                'title' : <article's title XPATH>
                'posted_date' : <article's posted date XPATH>
                }
        driver (selenium driver type):
            driver object

    Returns
        res ([]):
            res [<title<,<url>,<link URL>,<posted date>]

    Raises
        Exception
             when it catches an error
    """
    try:
        soup = get_bs4_soup(response.url, driver)
        elements = xpaths["global"].split(",")
        raw = soup.find_all(elements[0], class_=elements[1])
        res = []
        for html in raw:
            url = response.urljoin(get_bs4_url(html, xpaths["link"]))
            title = get_text_bs4(html, xpaths["title"])
            date = get_text_bs4(html, xpaths["posted_date"])
            res.append(dict(url=unquote(url), title=title, posted_date=date))
        return res
    except Exception:
        return None


def get_bs4_data_from_response(response, data, xpaths, driver):
    """
    Scrape the page content from response object.

    Args
        response (response object):
            Request response content
        xpaths dict(json):
            xpaths {
                'global' : <page html block XPATH ofr each article>
                'title' : <article's title XPATH>
                'posted_date' : <article's posted date XPATH>
                }
        driver : selenium driver type
            driver object

    Returns
        text (string):
            formated html content

    Raises
        Exception
             when it catches  error
    """
    try:
        elements = xpaths["statement"].split(",")
        soup = remove_unwanted_tags(response.url, driver, xpaths)
        if soup is None:
            soup = get_bs4_soup(response.url, driver)
        raw = soup.find_all(elements[0], class_=elements[1])
        text = []
        for txt in raw:
            text.append(txt.get_bs4_text())
        text = "\n".join(text)
    except Exception:
        pass
    finally:
        if text is None:
            text = html_utils.get_bs4_response_content(response, xpaths)

        # ger date
        date = data["posted_date"]
        if date is None:
            date = get_bs4_text(soup, xpaths["posted_date"])
        else:
            date = dates_parser.get_date(data, response, xpaths)
        return html_utils.format_html_text(text), date


def get_bs4_url(html, element):
    """
    Scrape  link URL from response content.

    Args
        html : html (Beautifulsoup object):
               html content
        element : Beautifull soup element ID

    Returns
        text (string)
            link URL
    Raises
        Exception
             when it catches  error

    """
    try:
        dispatcher = {
            "html.a": href_html_a_bs4,
            "html.span": href_html_span_bs4,
            "html.h2.a": href_html_h2_a_bs4,
            "html": href_html_bs4,
            "html_h3_a": href_html_h3_a_bs4,
            "html_h6_a": href_html_h6_a_bs4,
            "html_li_a": href_html_li_a_bs4,
            "html_li": href_html_li_bs4,
        }

        text = fire_me(dispatcher[element], html)

        return text
    except Exception:
        pass


def href_html_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.a["href"]).

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text (string):
            link url
    """
    return html.a["href"]


def href_html_span_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.span["href"]).

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text (string):
            link url
    """
    return html.span["href"]


def href_html_h2_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.h2.a["href"]).

    Args
       html (Beautifulsoup object):
             html content

    Returns
        text (string):
            link url
    """
    return html.h2.a["href"]


def href_html_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html["href"]).

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text (string):
            link url
    """
    return html["href"]


def href_html_li_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.li.a["href"]).

    Args
       html (Beautifulsoup object):
            html content

    Returns
        text (string):
            link url
    """
    return html.li.a["href"]


def href_html_h3_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.h3.a["href"]).

    Args
       html (Beautifulsoup object):
            html content

    Returns
        text (string):
            link url
    """
    return html.h3.a["href"]


def href_html_h6_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.h6.a["href"]).

    Args
       html (Beautifulsoup object):
            html content

    Returns
        text (string):
            link url
    """
    return html.h6.a["href"]


def href_html_li_a_(html):
    """
    This function scrapes html from Beautifulsoup object using element(html.li.a["href"]).

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text: string
            link url
    """
    return html.li.a["href"]


def href_html_li_bs4(html):
    """
    This function scrapes link  using element(html.li["href"]).

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text (string):
            link url
    """
    return html.li["href"]


def get_text_bs4(html, element):
    """
    This function scrapes html from Beautifulsoup object.

    Args
        html (Beautifulsoup object):
             html content

        element : beautifull soup element Tag ID

    Returns
        text (string)
            html text

    Raises
        Exception
             when it catches  error

    """
    try:
        dispatcher = {
            "html.text": html_text_bs4,
            "html.a": html_a_bs4,
            "html.a_span": html_a_span_bs4,
            "html.span": html_span_bs4,
            "html.h1": html_h1_bs4,
            "html.h1_a": html_h1_a_bs4,
            "html.h2": html_h2_bs4,
            "html.h2_a": html_h2_a_bs4,
            "html.h3": html_h3_bs4,
            "html.h3_a": html_h3_a_bs4,
            "html.h6_a": html_h6_a_bs4,
            "html.h4": html_h4_bs4,
            "html.h4_a": html_h4_a_bs4,
            "strong": strong_bs4,
            "html.strong": html_strong_bs4,
            "html.time": html_time_bs4,
            "html.div": html_div_bs4,
            "html.small": html_small_bs4,
            "html.li_a": html_li_a_bs4,
            "html.li": html_li_bs4,
        }

        elements = element.split(",")
        if len(elements) > 1:
            return (html.find(elements[0], class_=elements[1]).text).strip()
        text = fire_me(dispatcher[element], html)
        return text
    except Exception:
        pass


def fire_me(func_name, html):
    """
     Call function based on func_name.

    Args
        func_list : list of function to call

    Returns
        text (string)
            html text
    """
    return func_name(html)


# below names of function
def html_text_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.text


def html_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[]..

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.a.text


def html_a_span_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[]..

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.a.span.text


def html_span_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[]..

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.span.text


def html_h1_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[]..

    Args
         html (Beautifulsoup object):
               html content

    Returns
        text (string):
            html text
    """
    return html.h1.text


def html_h1_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[ html.h1.a.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.h1.a.text


def html_h2(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.h2.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.h2.text


def html_h2_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.h2.a.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.h2.a.text


def html_h3_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.h3.text].

    Args
         html (Beautifulsoup object):
               html content

    Returns
        text (string):
            html text
    """
    return html.h3.text


def html_h3_a_bs4(html):
    return html.h3.a.text


def html_h6_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.h3.a.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.h6.a.text


def html_h4_bs4(html):
    """
    This function scrapes html from Beautifulsoup object using  elt[html.h4.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text: string
            html text
    """
    return html.h4.text


def html_h4_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.h4.a.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.h4.a.text


def strong_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.strong.text].

     Args
          html (Beautifulsoup object):
               html content

     Returns
         text (string):
             html text
    """
    return html.strong.text


def html_strong_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.strong.text].

    Args
         html (Beautifulsoup object):
               html content

    Returns
        text (string):
            html text
    """
    return html.strong.text


def html_time_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.time.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.time.text


def html_div_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.div.text].

    Args
         html (Beautifulsoup object):
              html content

    Returns
        text (string):
            html text
    """
    return html.div.text


def html_small_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[ html.small.text].

    Args
        html (Beautifulsoup object):
          statement content

    Returns
        text (string):
            html text
    """
    return html.small.text


def html_li_a_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.li.a.text].

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text (string):
            html text
    """
    return html.li.a.text


def html_li_bs4(html):
    """
    This function scrapes html from Beautifulsoup  using  elt[html.li.text].

    Args
        html (Beautifulsoup object):
             html content

    Returns
        text (string):
            html text
    """
    return html.li.text
