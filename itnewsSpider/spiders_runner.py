from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from itnewsSpider.spiders import ftchinese, huxiu, solidot

process = CrawlerProcess(get_project_settings())

process.crawl(huxiu.Huxiu)
process.crawl(ftchinese.Ftchinese)
process.crawl(solidot.Solidot)
# the script will block here until the crawling is finished
process.start()
