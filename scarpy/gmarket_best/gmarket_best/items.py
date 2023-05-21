# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 딕셔너리 느낌
class GmarketBestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 상품명, 정가, 할인가, 할인율, 상세링크
    title = scrapy.Field()
    s_price = scrapy.Field()
    o_price = scrapy.Field()
    discount_rate = scrapy.Field()
    link = scrapy.Field()
