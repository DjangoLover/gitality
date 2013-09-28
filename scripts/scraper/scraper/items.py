from scrapy.item import Item, Field


class DjangodashItem(Item):
    repo = Field()
    nicks = Field()
    team = Field()
