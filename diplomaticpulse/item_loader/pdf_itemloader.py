"""
This module implements generic Item_loader builder.
"""
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.utils.project import get_project_settings
from diplomaticpulse.items import StatementItem
from diplomaticpulse.misc import (
    cookies_utils,
    utils,
)
from diplomaticpulse.parsers import pdf_parser, dates_parser, html_parser

def itemloader(response, data, xpaths):
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
        Dict : ( Iterable of Items)
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
    statement = raw["statement"] if raw else None
    item["statement"] = html_parser.format_html_text(statement)
    item["posted_date"] = dates_parser.get_date_from_pdf(
        data["posted_date"], raw, item["statement"], item["title"]
    )
    return item


