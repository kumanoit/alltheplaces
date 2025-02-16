import json

from scrapy.spiders import SitemapSpider

from locations.hours import OpeningHours, sanitise_day, DAYS_DE
from locations.structured_data_spider import StructuredDataSpider


class RossmannDESpider(SitemapSpider, StructuredDataSpider):
    name = "rossmann_de"
    item_attributes = {"brand": "Rossmann", "brand_wikidata": "Q316004"}
    allowed_domains = ["www.rossmann.de"]
    download_delay = 0.2
    sitemap_urls = ["https://www.rossmann.de/de/filialen/sitemap.xml"]
    sitemap_rules = [("", "parse_sd")]

    def sitemap_filter(self, entries):
        for entry in entries:
            if not entry["loc"].endswith("/index.html"):
                yield entry

    def pre_process_data(self, ld_data, **kwargs):
        ld_data["name"] = ld_data["name"].split("\n")[0]
        ld_data["image"] = None

    def post_process_item(self, item, response, ld_data, **kwargs):
        if ohjs := response.xpath("//@data-openingtimes").get():
            ohjs = json.loads(ohjs)
            oh = OpeningHours()
            for day, times in ohjs.items():
                day_en = sanitise_day(day, DAYS_DE)
                for time in times:
                    oh.add_range(day_en, time["openTime"], time["closeTime"])
            item["opening_hours"] = oh.as_opening_hours()

        yield item
