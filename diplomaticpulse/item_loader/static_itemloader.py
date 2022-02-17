"""
This module implements generic Item_loader builder.
"""
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from diplomaticpulse.items import StatementItem
from diplomaticpulse.parsers import dates_parser, html_parser
from diplomaticpulse.misc import utils


def itemloader(response, data, xpaths):
    """
    This method builds an Item object (static content).

    Args:
        response (response (Response object) – the response being processed)
         content to parse
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
        Item_loader

    """
    Item_loader = ItemLoader(item=StatementItem(), response=response)
    Item_loader.default_input_processor = MapCompose(str())
    Item_loader.default_output_processor = TakeFirst()
    Item_loader.add_value("posted_date", dates_parser.get_date(data, response, xpaths))
    Item_loader.add_value("url", utils.check_url(response.url))

    Item_loader.add_value(
        "title", html_parser.get_title(data["title"], response, xpaths)
    )
    statement = html_parser.get_html_response_content(response, xpaths["statement"])
    Item_loader.add_value("statement", statement)
    return Item_loader
