"""
  This implements Scrapy pipeline DropItemPipeline.
"""
from scrapy.exceptions import DropItem


class DropItemPipeline(object):
    """
    This class drops an empty item before being saved into elasticsearch.

    """

    @classmethod
    def process_item(self, item, spider):
        """
        This method throws an excpetion when the statement in the item is NULL.

        Args
          item: object of item

        Returns
          item: object of item

        Raises
         DropItem
           when statement is None

        """
        if not item["statement"]:
            raise DropItem("Item dropped because the statement is None or empty")
        return item