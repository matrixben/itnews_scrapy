import scrapy
import datetime
from itnewsSpider import items


class Huxiu(scrapy.Spider):
    name = 'huxiu'
    allowed_domains = ['huxiu.com']
    start_urls = ['https://www.huxiu.com']

    def parse(self, response):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #实现网页解析
        for itnews in response.xpath('//*[@id="index"]//div[contains(@class, "mod-b")]'):
            huxiu_news = items.ItnewsspiderItem()
            huxiu_news['title'] = itnews.xpath('.//h2/a/text()').extract_first()
            huxiu_news['tag'] = itnews.xpath('.//a[@class="column-link"]/text()').extract_first()
            sub_url = itnews.xpath('.//h2/a/@href').extract_first()
            huxiu_news['source_url'] = response.urljoin(str(sub_url))
            huxiu_news['publish_date'] = current_date
            yield huxiu_news
