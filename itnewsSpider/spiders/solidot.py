import scrapy
import datetime
from itnewsSpider import items


class Solidot(scrapy.Spider):
    name = 'solidot'
    allowed_domains = ['solidot.org']
    start_urls = ['https://www.solidot.org']

    def parse(self, response):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #实现网页解析
        for itnews in response.xpath('//*[@id="center"]/div[@class="block_m"]'):
            solidot_news = items.ItnewsspiderItem()
            solidot_news['title'] = itnews.xpath('.//h2/a/text()').extract_first()
            solidot_news['tag'] = itnews.xpath('.//*[@class="icon_float"]/a/@title').extract_first()
            sub_url = itnews.xpath('.//h2/a/@href').extract_first()
            solidot_news['source_url'] = response.urljoin(str(sub_url))
            solidot_news['publish_date'] = current_date
            yield solidot_news