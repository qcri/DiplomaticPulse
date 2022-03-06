"""
This module implements cookies.
"""
def get_cookies(xpaths):
    """
    This method reads request cookies.

    Args:
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
        for ck in xpaths["cookies"].split(";"):
                cookies[ck.split("=")[0].strip()] = str(ck.split("=")[1].strip())
        return cookies
    except Exception:
        return None
