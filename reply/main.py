import requests
import json
from google.cloud import firestore
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

CHANNEL_ACCESS_TOKEN = "ACCESS_TOKEN"
CHANNEL_SECRET = "SECRET"

# Channel Access Token
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(CHANNEL_SECRET)


def callback(request):
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# handle message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    db = firestore.Client('FIRESTORE_PROJECT_ID')
    horoscope = {
        '魔羯', '水瓶', '雙魚', '牡羊', '金牛', '雙子', '巨蟹', '獅子', '處女', '天秤', '天蠍', '射手'
    }
    if event.message.text.lower() == "bye":
        db.collection(u'COLLECTION_NAME').document(event.source.user_id).delete()
        message = TextSendMessage(text=u'退訂成功！希望未來還有機會為您服務')
        line_bot_api.reply_message(event.reply_token, message)

    if event.message.text[:2] in horoscope:
        horoscope = event.message.text[:2] + '座'
        doc_ref = db.collection(u'COLLECTION_NAME').document(event.source.user_id)
        doc_ref.set({u'horoscope': event.message.text[:2]})

        message = TextSendMessage(
            text=u'嗨！' + horoscope + '的朋友，《祝你好運》每天為您準備當日運勢，用好運開啟每一天！' +
            '\n\n' + get_todays_luck(horoscope))
        line_bot_api.reply_message(event.reply_token, message)


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
