import scrapy

class TigerBookItem(scrapy.Item):

    제목 = scrapy.Field()
    글 = scrapy.Field()
    그림 = scrapy.Field()
    출판사 = scrapy.Field()
    책소개 = scrapy.Field()
    작가최근작 = scrapy.Field()
    정가 = scrapy.Field()
    판매가 = scrapy.Field()
    책표지 = scrapy.Field()
    URL= scrapy.Field()



