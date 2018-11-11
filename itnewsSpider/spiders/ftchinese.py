import scrapy
import datetime
from itnewsSpider import items


class Ftchinese(scrapy.Spider):
    name = 'ftchinese'
    allowed_domains = ['ftchinese.com']
    start_urls = ['http://www.ftchinese.com']

    def parse(self, response):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #实现网页解析,url中包含story的是免费文章, premium是付费文章
        for itnews in response.xpath("//div[contains(@class, 'list-container')]")[1]\
                              .xpath(".//div[contains(@class, 'item-container')]"):
            ftchinese_news = items.ItnewsspiderItem()
            ftchinese_news['title'] = itnews.xpath('.//h2/a/text()').extract_first()
            ftchinese_news['tag'] = itnews.xpath('.//h2/div[@class="item-tag"]/a/text()').extract_first()
            sub_url = itnews.xpath('.//h2/a/@href').extract_first()
            if 'story' not in str(sub_url):
                continue
            ftchinese_news['source_url'] = response.urljoin(str(sub_url))
            ftchinese_news['publish_date'] = current_date
            yield ftchinese_news
