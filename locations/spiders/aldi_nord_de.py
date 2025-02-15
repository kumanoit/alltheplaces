# -*- coding: utf-8 -*-
from scrapy import Spider

from locations.dict_parser import DictParser
from locations.hours import OpeningHours, DAYS


# Does have Linked Data, but requires JS to load it
class AldiNordDESpider(Spider):
    name = "aldi_nord_de"
    item_attributes = {"brand": "ALDI Nord", "brand_wikidata": "Q41171373"}
    start_urls = [
        "https://uberall.com/api/storefinders/ALDINORDDE_UimhY3MWJaxhjK9QdZo3Qa4chq1MAu/locations/all"
    ]

    def parse(self, response, **kwargs):
        for store in response.json()["response"]["locations"]:

            store["street_address"] = ", ".join(
                filter(None, [store.pop("streetAndNumber", store.pop("addressExtra"))])
            )

            item = DictParser.parse(store)

            oh = OpeningHours()
            for rule in store["openingHours"]:
                if rule.get("closed", False):
                    continue
                oh.add_range(DAYS[rule["dayOfWeek"] - 1], rule["from1"], rule["to1"])
            item["opening_hours"] = oh.as_opening_hours()

            yield item
