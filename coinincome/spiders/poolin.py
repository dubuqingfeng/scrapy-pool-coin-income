# -*- coding: utf-8 -*-
import scrapy
import json

###
# https://api-prod.poolin.com/api/public/v2/basedata/coins/block_stats
###
from coinincome.items import CoinincomeItem
from coinincome.utils import calculate_unit


class PoolinSpider(scrapy.Spider):
    name = 'poolin'
    allowed_domains = ['poolin.com']
    start_urls = ['https://api-prod.poolin.com/api/public/v2/basedata/coins/block_stats']

    def parse(self, response):
        response_body = json.loads(response.body)
        if response_body['err_no'] == 0:
            for coin in response_body['data']:
                item = CoinincomeItem()
                item['coin'] = coin.lower()
                item['income_coin'] = float(response_body['data'][coin]['rewards_per_unit'])
                item['income_hashrate_unit'] = response_body['data'][coin]['reward_unit']
                item['income_hashrate_unit_num'] = calculate_unit(response_body['data'][coin]['reward_unit'])
                item['next_income_coin'] = 0
                item['pool_name'] = self.name
                item['request_url'] = response.url
                yield item
