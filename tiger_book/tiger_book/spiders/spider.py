from glob import glob
import scrapy
import re
import json

key = ('호랑이 그림책')
# KEYWORD = input('찾고 싶은 키워드를 입력해주세요 (키워드는 띄어쓰기로 구분 됩니다) : ').split(' ')

KEYWORD = key.split(' ')

while True:

    BOOKTYPE = input('키워드가 제목에만 있는걸 원할시 1번, 제목에는 없지만 본문내용과 관련 있는걸 원한다면 2번을 눌러주세요 : ')

    if BOOKTYPE == '1' or BOOKTYPE == '2':
        break

INPUTKEY = '+'.join(KEYWORD)

URL = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord='+INPUTKEY+'&ViewRowCount=25&page=1'

#https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord=호랑이&ViewRowCount=25&page=1

PAGE_URL = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord='+INPUTKEY+'&ViewRowCount=25&page={}'

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    start_urls = [URL]
    
    def parse(self, response):
        
        NUM = 1

        #한 페이지 이상
        LONG = response.xpath('//*[@id="short"]/div[12]/a')

        if LONG == []:

            while 1 :

                page = response.xpath(f' //*[@id="short"]/div[{NUM}]/a/@href').extract()

                if page == []:

                    break

                NUM += 1
                
            PAGE = NUM-2

            for i in range(1,PAGE+1):

                PAGE_URLS = PAGE_URL.format(i)

                yield scrapy.Request(PAGE_URLS, self.detail_parse)

        #한 페이지
        if LONG != []:

            page = response.xpath('//*[@id="short"]/div[12]/a/@href').extract()        

            page_num = page[0]

            PAGE_NUM = re.sub(r'[^0-9]','',page_num)

            PAGE = int(PAGE_NUM)

            for i in range(1,PAGE+1):
                
                PAGE_URLS = PAGE_URL.format(i)

                #print(PAGE_URLS)

                yield scrapy.Request(PAGE_URLS, self.detail_parse)

    def detail_parse(self,response):

        for i in range(1,26):

            detail_page =  response.xpath(f'//*[@id="Search3_Result"]/div[{i}]/table').extract()

            if detail_page != []:

                detail_page_split = detail_page[0].split('<')   

                BOOKID = re.sub(r'[^0-9]','',detail_page_split[25])   

                BOOK_URL = (f'https://www.aladin.co.kr/shop/wproduct.aspx?ItemId={BOOKID}')

               # print(BOOK_URL)

                yield scrapy.Request(BOOK_URL, self.book_parse)

    def book_parse(self,response):

        two_List = []

        # 키워드가 제목에 포함
        if BOOKTYPE == '1' :

            title = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[2]/div/a[1]/text()')[0].extract()  

            for i in KEYWORD:

                if i in title:
                    
                    print(title)

        # 키워드가 제목에 포함 되어있지많을 경우
        if BOOKTYPE == '2':
            
            title = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[2]/div/a[1]/text()')[0].extract()

            for i in KEYWORD:
        
                if i not in title:

                    two_List.append(title)
            
            if len(two_List) == len(KEYWORD) :

                No_title = two_List[0]

                print(response, No_title)





   
                    
                
  



                # for num in range(1,15):

                #         html = response.xpath(f'/html/head/meta[{num}]').get()
                        
                #         html_List = html.split('"')

                #         meta_name = html_List[1]

                #         if meta_name == 'description' :

                #             body_num = num

                #             body_html = response.xpath(f'/html/head/meta[{body_num}]').get()

                #             body_List = body_html.split('"')

                #             summary = body_List[3]

                #             if key in summary:

                #                 #print(summary)

                #                 title = response.xpath('//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[2]/div/a[1]/text()')[0].extract()

                #                 print(key,title)


    
            
            

            
       


            

            

           

