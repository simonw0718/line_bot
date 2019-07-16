#寫servor接收line轉過來的訊息
#SDK (software development kits)--系統的套裝軟體 
# python 寫網站的套件 flask & django
# webhooks -> 連結網站跟app
# 以下程式碼是寫網頁用的(flask)的語法

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    StickerSendMessage
)

app = Flask(__name__)

#存取權限來跟line互動
line_bot_api = LineBotApi('vky70sNW0Z/J63o1GXjWHFAhU+9BKDeVlK4jOAtxUNtt5c9FfzRL+L4KG3ifrGsGALCWs8vxhigu6fYESrE9aMEp1qajrMdzHy1GfQIIDANmOieYEdFK4vKaBQM0PV1i3zGJFJX3TwknOhvahOv0qwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5bbff692a4d4fece0a72d95b7d6aed38')

#有人來"/callback" (連結到這個網址) 就會觸發callback()
#在line系統上設定好要連結的網址，這樣才會在接收訊息之後去跟app.py互動

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#觸發完callback之後再觸發handle_message
#這種完整訊息通常都不用改

#以下處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    reply_text = '聽不懂R'
    sticker = StickerSendMessage(
        package_id='1',
        sticker_id='1'
    )

    if '給我貼圖' in msg:
        line_bot_api.reply_message(
        event.reply_token,sticker)
    return


    if msg in ['Hi', 'hi']:
        reply_text = 'Yo'
    elif msg in ['你好','哩賀']:
        reply_text = '哩賀'
    else:
        reply_text = '聽不懂R'
        sticker = StickerSendMessage(
        package_id='1',
        sticker_id='2'
    )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(reply_text))
    

#通常會把code寫成main function，寫下面這行是希望直接讀取才執行
#避免import app.py的時候就開始跑
if __name__ == "__main__": 
    app.run()