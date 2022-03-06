"""
This module implements generic StatementItem builder.
"""
from diplomaticpulse.items.items import StatementItem
from diplomaticpulse.parsers import pdf_parser, dates_parser, html_parser


def loader(response, data, xpaths):
    """
     This method constructs Scrapy StatementItem object.

    Parameters:
        response : response (Response object) – the response being processed

        data : dict(String)
            Python dict in the following format:
               data{
                    'title' : <title of the article>
                    'posted_date' : <published date of article >
               }
        xpaths : dict(String)
                 Python dict in the following format:
                 xpaths{
                    'title' : <xpath of the title>
                    'posted_date' : <xpath of the posted_date>
                    'statement' : <xpath of the statement>

               }
    Returns:
        Dict : ( Iterable of items)
        Python dict in the following format:
          {
            'title' : <title of the article>
            'statement' : <article statement content>
            'posted_date' :<article published date>
          }

    """

    item = StatementItem()
    item["title"] = html_parser.get_title(data["title"], response, xpaths)
    raw = pdf_parser.parse_pdfminer(response.url)
    item["statement"] = raw["statement"] if raw else None
    item["posted_date"] = dates_parser.get_date_from_pdf(
        data["posted_date"], raw, item["statement"], item["title"]
    )
    return item
