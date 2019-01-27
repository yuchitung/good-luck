from google.cloud import firestore
import requests
import json
from linebot import (LineBotApi)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)


def publish_luck(event, context):
    try:
        CHANNEL_ACCESS_TOKEN = "ACCESS_TOKEN"
        CHANNEL_SECRET = "SECRET"
        db = firestore.Client('FIRESTORE_PROJECT_ID')
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        docs = db.collection(u'COLLECTION_NAME').get()
        for doc in docs:
            horoscope = doc.to_dict()['horoscope'] + '座'
            line_bot_api.push_message(
                doc.id, TextSendMessage(text=get_todays_luck(horoscope)))
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')


def get_todays_luck(horoscope):
    luck_collection = {}
    response = requests.get(
        'https://horoscope-crawler.herokuapp.com/api/horoscope')
    data = json.loads(response.text)
    for value in data:
        luck_collection[value['name'][5:]] = value
    luck = luck_collection[horoscope]
    todays_luck='今日短評：'+luck['TODAY_WORD']+'\n' \
                    +'幸運色：'+ luck['LUCKY_COLOR']+'\n\n' \
                    + luck['STAR_ENTIRETY']+ luck['DESC_ENTIRETY']+'\n\n' \
                    + luck['STAR_LOVE'] + luck['DESC_LOVE']+'\n\n' \
                    + luck['STAR_MONEY'] + luck['DESC_MONEY'] +'\n\n'\
                    + luck['STAR_WORK'] + luck['DESC_WORK'] +'\n\n'\
                    + 'Reference - 紫微科技網'
    return todays_luck
