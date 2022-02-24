"""
This module implements generic Item_loader builder.
"""
from diplomaticpulse.items.items import StatementItem
from diplomaticpulse.parsers import pdf_parser, dates_parser, html_parser


def loader(response, data, xpaths):
    """
    This is the specified callback used by Scrapy to process downloaded responses.

    Parameters:
        response : response (Response object) – the response being processed

        data  : dict(String)
                Python dict in the following format:
               data{
               'title' : <title of the article>
               'posted_date' : <article published date>
               }

    Returns:
        Dict : ( Iterable of items)
        Python dict in the following format:
          {
            'link' : <article URL>
            'title' : <title of the article>
            'statement' : <article statement content>
            'posted_date' :<article published date>
            'indexed_date' :<article indexed date>
            'country' : <country name>
            'parent_url' : <parent url (country overview page URL)>
            'content_type' : response content type>
          }

    """

    item = StatementItem()
    item["title"] = html_parser.get_title(data["title"], response, xpaths)
    raw = pdf_parser.parse_pdfminer(response.url, None)
    item["statement"] = raw["statement"] if raw else None
    item["posted_date"] = dates_parser.get_date_from_pdf(
        data["posted_date"], raw, item["statement"], item["title"]
    )
    return item
