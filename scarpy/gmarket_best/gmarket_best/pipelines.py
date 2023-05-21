# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests
import json

class GmarketBestPipeline:
    # 크롤링 된 아이템을 최종적으로 후처리
    def process_item(self, item, spider): # yield된 결과 하나하나씩 item으로 들어옴
        keyword = "봄"
        if keyword in item["title"]:
            msg = f"{keyword}알림! // {item['title']}, {item['s_price'], {item['link']}}😫"
            self.__send_slack(msg)
        return item

    # 슬랙에 알림보내는 메소드
    def __send_slack(self, msg):
        WEBHOOK_URL = "https://hooks.slack.com/services/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"

        payload = {
            "channel": "#랜덤",
            "username": "?",
            "text": msg
        }

        print("payload", payload)

        requests.post(WEBHOOK_URL, json.dumps(payload))