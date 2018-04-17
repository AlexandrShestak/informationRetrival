import scrapy
import urllib

from scrapy import Item, Field


class WikipediaItem(Item):
    id = Field()
    url = Field()
    title = Field()
    links = Field()
    snippet = Field()
    pass


class WikiSpider(scrapy.Spider):
    """
    the Page Spider for wikipedia
    """

    name = "wikipedia_ru"
    allowed_domains = ["wikipedia.org"]

    urls_dict = {}

    def start_requests(self):
        with open('../urlid.csv', 'rb') as file:
            for row in file:
                self.urls_dict['https://ru.wikipedia.org' + row[row.find(',') + 1:-1]] = row[:row.find(',')]
                # self.urls_dict[row[:row.find(',')]] = 'https://ru.wikipedia.org' + row[row.find(',') + 1:-1]
                # yield scrapy.Request('https://ru.wikipedia.org' + row[row.find(',') + 1:-1], self.parse)
        for key, value in self.urls_dict.iteritems():
            print value
            yield scrapy.Request(key, self.parse)
            break

    def parse(self, response):
        item = WikipediaItem()

        item['id'] = self.urls_dict[response.url]
        item['url'] = urllib.unquote(response.url)
        item['title'] = response.xpath('//h1/text()')[0].extract()
        # item['snippet'] = response.xpath('string(//div[@id="mw-content-text"]//p[1])').extract_first()[:255]
        # item['links'] = [response.urljoin(link) for link in response.xpath(self.links_xpath).xpath('@href').extract()
        #                  if self.allow_links.match(link) and not self.deny_links.match(link)]

        return item
