"""
This module implements cookies
"""


def get_cookies(xpaths):
    """
    Get request cookies.

    crawler_settings
        xpaths dict(json):
               xpaths{
                   'cookies' :<cookies>
                }

    Returns
         dict(json):
         cookies {
          'cookies' : <cookies>'
          }

    Raises
        Exception
             when it catches  error

    """
    try:
        cookies = {}
        for i in xpaths["cookies"].split(";"):
                cookies[i.split("=")[0].strip()] = str(i.split("=")[1].strip())
        return cookies
    except KeyError:
        return cookies
