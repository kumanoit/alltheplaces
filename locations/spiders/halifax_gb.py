from scrapy.spiders import SitemapSpider

from locations.structured_data_spider import StructuredDataSpider


class HalifaxGB(SitemapSpider, StructuredDataSpider):
    name = "halifax_gb"
    item_attributes = {"brand": "Halifax", "brand_wikidata": "Q3310164"}
    sitemap_urls = ["https://branches.halifax.co.uk/sitemap.xml"]
    sitemap_rules = [
        (r"https:\/\/branches\.halifax\.co\.uk\/[-'\w]+\/[-'\/\w]+$", "parse_sd")
    ]
    wanted_types = ["BankOrCreditUnion"]

    def sitemap_filter(self, entries):
        for entry in entries:
            if not "event" in entry["loc"].lower():
                yield entry
