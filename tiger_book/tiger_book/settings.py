BOT_NAME = 'tiger_book'

SPIDER_MODULES = ['tiger_book.spiders']
NEWSPIDER_MODULE = 'tiger_book.spiders'

ROBOTSTXT_OBEY = False

#로그 모아둔 파일
LOG_FILE = 'book.log'

#파일 인코딩
FEED_EXPORT_ENCODING = "utf-8-sig"

#item 정렬
FEED_EXPORT_FIELDS = ['제목','글','그림','출판사','정가','판매가','URL','책소개']


