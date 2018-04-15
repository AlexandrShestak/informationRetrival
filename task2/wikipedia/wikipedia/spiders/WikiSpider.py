# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Item, Field


class WikipediaItem(Item):
    url = Field()
    title = Field()
    links = Field()
    snippet = Field()
    pass


class WikiSpider(CrawlSpider):
    """
       The Page Spider for wikipedia
    """

    name = "wikipedia_spider"
    allowed_domains = ["wikipedia.org"]

    start_urls = [
        "https://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm",
        "https://en.wikipedia.org/wiki/Fuser_(Unix)",
        "https://en.wikipedia.org/wiki/Hyperparameter_optimization",
        "https://en.wikipedia.org/wiki/Machine_learning",
        "https://en.wikipedia.org/wiki/Information_retrieval"
    ]

    links_xpath = '(//div[@id="mw-content-text"]//a)[position() < 100]'
    allow_links = re.compile('/wiki/(?!((File|Talk|Category|Portal|Special|Template|Template_talk|Wikipedia|Help|Draft|MediaWiki):|Main_Page)).+')
    deny_links = re.compile('.*#.*')


    rules = (
        Rule(LinkExtractor(allow="https://en\.wikipedia\.org/wiki/(?!((File|Talk|Category|Portal|Special|Template|Template_talk|Wikipedia|Help|Draft|MediaWiki):|Main_Page)).+",
                           deny='.*#.*',
                           restrict_xpaths=links_xpath),
             callback='parse_wikipedia_page', follow=True),
    )

    def parse_wikipedia_page(self, response):
        item = WikipediaItem()

        item['url'] = response.url
        item['title'] = response.xpath('//h1/text()')[0].extract()
        item['snippet'] = response.xpath('string(//div[@id="mw-content-text"]//p[1])').extract_first()[:255]
        item['links'] = [response.urljoin(link) for link in response.xpath(self.links_xpath).xpath('@href').extract()
                         if self.allow_links.match(link) and not self.deny_links.match(link)]

        return item