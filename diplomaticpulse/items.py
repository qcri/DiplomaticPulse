"""
This module Srcapy Item
"""
import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


class StatementItem(scrapy.Item):
    """A class which allows defining item fields,

    Args
        Item(scrapy.Item class)

    Returns
          instance id Item

    """

    # article's title
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    # article's statement
    statement = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )

    # article's indexed date
    indexed_date = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    # article's posted date
    posted_date = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    # article's url
    url = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    # article's content type
    content_type = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    # article's language
    language = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    # article's country
    country = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )

    # article's parent url
    parent_url = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
