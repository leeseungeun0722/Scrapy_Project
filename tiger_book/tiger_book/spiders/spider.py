import scrapy
import re
from tiger_book.items import TigerBookItem

KEYWORD = input('찾고 싶은 키워드를 입력해주세요 (키워드는 띄어쓰기로 구분 됩니다) : ').split(' ')

# key = ('호랑이 그림책')
# KEYWORD = key.split(' ')

while True:

    BOOKTYPE = input('키워드가 제목에만 있는걸 원할시 1번, 제목에는 없지만 본문내용과 관련 있는걸 원한다면 2번을 눌러주세요 : ')

    if BOOKTYPE == '1' or BOOKTYPE == '2':

        break

INPUTKEY = '+'.join(KEYWORD)

#https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord=호랑이+그림책&ViewRowCount=25&page=1

URL = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord='+INPUTKEY+'&ViewRowCount=25&page=1'

# 시작 URL 만들기
PAGE_URL = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord='+INPUTKEY+'&ViewRowCount=25&page={}'

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    start_urls = [URL]
    
    def parse(self, response):
        
        NUM = 1

        # 페이지 자동 넘기기
        LONG = response.xpath('//*[@id="short"]/div[12]/a')

        # 1 페이지 부터 12 페이지 없을 경우
        if LONG == []:

            while 1 :
                
                #페이지 수 확인
                page = response.xpath(f'//*[@id="short"]/div[{NUM}]/a/@href').extract()

                #페이지 수가 오버 되어 출력값이 []라면
                if page == []:

                    break
                
                # 페이지 수 계속 올리기
                NUM += 1
            
            # 최총 페이지 수
            PAGE = NUM-2

            # 총 몇페이지 까지 있는지 확인했으니 1페이지 부터 마지막 페이지 까지 돌기
            for i in range(1,PAGE+1):

                #https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord=호랑이+그림책&ViewRowCount=25&page=1
                PAGE_URLS = PAGE_URL.format(i)

                yield scrapy.Request(PAGE_URLS, self.detail_parse)

        # 만약 12페이지 이상일 경우
        #https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord=호랑이&ViewRowCount=25&page=1
        if LONG != []:

            page = response.xpath('//*[@id="short"]/div[12]/a/@href').extract()[0]     

            # 숫자만 추출 -> 최종 페이지 수가 나온다. 
            PAGE = int(re.sub(r'[^0-9]','',page))

            #첫 페이지 부터 마지막 페이지 까지 URL 추출
            for i in range(1,PAGE+1):
                
                PAGE_URLS = PAGE_URL.format(i)

                yield scrapy.Request(PAGE_URLS, self.detail_parse)

    def detail_parse(self,response):

        #한 페이지 안에 세부 책 정보로 들어가는 세부 URL 추출.
        for i in range(1,26):

            detail_page =  response.xpath(f'//*[@id="Search3_Result"]/div[{i}]/table').extract()

            if detail_page != []:
                
                #BOOKID 추출
                detail_page_split = detail_page[0].split('<')   

                BOOKID = re.sub(r'[^0-9]','',detail_page_split[25])   

                #세부 페이지 URL
                #https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=269644239
                BOOK_URL = (f'https://www.aladin.co.kr/shop/wproduct.aspx?ItemId={BOOKID}')

                yield scrapy.Request(BOOK_URL, self.book_parse)

    def book_parse(self,response):

        item = TigerBookItem()

        two_List = []
    
        title = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[2]/div/a[1]/text()')[0].extract()

        BOOKID =  response.xpath('/html/head/link[1]/@href')[0].extract().split('=')[1]
        
        # 줄거리 추출
        for num in range(1,15):
            
            html = response.xpath(f'/html/head/meta[{num}]').get()
                            
            meta_name = html.split('"')[1]

            if meta_name == 'description' :

                body_html = response.xpath(f'/html/head/meta[{num}]').get()

                summary = body_html.split('"')[3] 

        # 키워드가 제목에 포함 되어있을 경우
        for i in KEYWORD:

            if i in title:
                    
                item['제목'] = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[2]/div/a[1]/text()')[0].extract()
                    
                item['글'] = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[3]/a[1]/text()')[0].extract()

                item['그림'] = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[3]/a[2]/text()')[0].extract()

                item['출판사'] = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[3]/a[3]/text()')[0].extract()

                item['책소개'] = summary

                item['정가'] = response.xpath('//*[@id="Ere_prod_allwrap"]/div[4]/div[4]/div/div[1]/ul/li[1]/div[2]/text()')[0].extract()

                item['판매가'] = response.xpath('//*[@id="Ere_prod_allwrap"]/div[4]/div[4]/div/div[1]/ul/li[2]/div[2]/span/text()')[0].extract() + '원'

                item['URL'] = (f'https://www.aladin.co.kr/shop/wproduct.aspx?ItemId={BOOKID}')

        #키워드가 제목에 포함 되어있지않지만 줄거리에는 포함될 경우
        if BOOKTYPE == '2':
            
            title = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[2]/div/a[1]/text()')[0].extract()

            for i in KEYWORD:
        
                if i not in title:

                    two_List.append(title)

            # 지정한 키워드 모두 제목에 포함 인될경우
            if len(two_List) == len(KEYWORD) :

                for i in KEYWORD:

                    if i in summary:

                        item['제목'] = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[2]/div/a[1]/text()')[0].extract()
                    
                        item['글'] = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[3]/a[1]/text()')[0].extract()

                        item['그림'] = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[3]/a[2]/text()')[0].extract()

                        item['출판사'] = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[3]/a[3]/text()')[0].extract()

                        item['책소개'] = summary

                        item['정가'] = response.xpath('//*[@id="Ere_prod_allwrap"]/div[4]/div[4]/div/div[1]/ul/li[1]/div[2]/text()')[0].extract()

                        item['판매가'] = response.xpath('//*[@id="Ere_prod_allwrap"]/div[4]/div[4]/div/div[1]/ul/li[2]/div[2]/span/text()')[0].extract() + '원'

                        item['URL'] = (f'https://www.aladin.co.kr/shop/wproduct.aspx?ItemId={BOOKID}')

            # 제목 x 본문 o          
            return item
        # 제목 o            
        return item
  

    
            
            

            
       


            

            

