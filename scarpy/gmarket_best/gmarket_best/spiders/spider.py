import scrapy
from gmarket_best.items import GmarketBestItem

class Spider(scrapy.Spider):

    # 얘네 3개는 꼭 필요
    name = 'GmarketBestSellers' # 스파이더의 이름(크롤러의 이름)
    allowed_domains = ['gmarket.co.kr'] # 크롤링할 웹사이트의 도메인, 이 도메인을 안벗어남, 다른 도메인은 제외 여기는 Gmarket만 naver는 안가
    start_urls = ['https://corners.gmarket.co.kr/BestSellers'] # 스크래이핑을 시작할 주소

    # 크롤링을 수행하여 item으로 만들어주는 메소드
    # start_urls로 요청을 보낸 결과(응답)가 들어온다.
    def parse(self, response): # response는 TextResponse이다.
        links = response.xpath(
            '//*[@id="gBestWrap"]/div/div[3]/div/ul/li/a/@href'
        ).extract()

        for link in links:
            # Request 객체를 만들어서 spider한테 던져줌. 그래서 return이 아닌 yield
            # parse가 Request 객체를 생성하는 generator가 됨.
            # callback : 작업결과를 어떻게 처리할지를 지정
            yield scrapy.Request(link, callback = self.page_content)

    # 상세페이지의 결과물을 items.py로 만들기로함
    def page_content(self, response):
        # 스크래이핑한 데이터를 저장할 GmarketBestItem
        item = GmarketBestItem()
        
        # item의 멤버변수의 이름과 키의 이름은 항상 일치해야한다.
        item["title"] = response.xpath(
            '//*[@id="itemcase_basic"]/div[1]/h1/text()'
        ).extract_first() # 제일 처음 값 한개만 가져오기

        item["s_price"] = response.xpath(
            '//*[@id="itemcase_basic"]/div[1]/p/span/strong/text()'
        ).extract_first().replace(",", "")

        try:
            item["o_price"] = response.xpath(
                '//*[@id="itemcase_basic"]/div[1]/p/span/span/text()'
            ).extract_first().replace(",", "")
        except:
            item["o_price"] = item["s_price"]

        item["discount_rate"] = str(
            round((1 - int(item["s_price"]) / int(item["o_price"]))*100, 2)) + "%"
        
        item["link"] = response.url  # 요청한 링크 얻기

        return item