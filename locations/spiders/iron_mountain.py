# -*- coding: utf-8 -*-
import scrapy
from locations.open_graph_parser import OpenGraphParser


class IronMountainSpider(scrapy.spiders.SitemapSpider):
    name = "iron_mountain"
    item_attributes = {
        "brand": "Iron Mountain Incorporated",
        "brand_wikidata": "Q1673079",
    }
    sitemap_urls = ["https://locations.ironmountain.com/robots.txt"]
    download_delay = 1.0

    def parse(self, response):
        item = OpenGraphParser.parse(response)
        if item["lat"]:
            yield item
