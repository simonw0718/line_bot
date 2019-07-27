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

## Oauth code 上半部 
from requests_oauthlib import OAuth2Session
    
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

# This information is obtained upon registration of a new GitHub
client_id = "1603016408"
client_secret = "0eb3f0d6e46b6429ad25884023728c04"
#domument中的url
authorization_base_url = 'https://access.line.me/oauth2/v2.1/authorize'
token_url = 'https://api.line.me/oauth2/v2.1/token'
#逐一修改
## Oauth code 上半部 


app = Flask(__name__)

#
app.config['SECRET_KEY'] = 'thesesecretkey'


## Oauth code 下半部##

#建立login的連結
#需要response_type, client_id, redirect_url(=callback路徑), state, scope(取得使用者那些資料,需取得profile & openid)

def get_redirect_url():
    return url_for('.oath_callback',
                   _external = True,  #external = trun才是public的
                   _scheme = 'https') #因為可以產生http or https
#上面fun會回傳oauth callback 路徑


@app.route("/login")
def login():
    line_login = OAuth2Session(client_id,
                               redirect_url = get_redirect_url(),
                               scope = 'profile openid')

    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)

#state ->字串, 防攻擊

@app.route("/oauth_callback")
def oauth_callback():
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    return jsonify(github.get('https://api.github.com/user').json())
## Oauth code 下半部##


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
    elif '換一張貼圖' in msg:
        sticker = StickerSendMessage(
        package_id='1',
        sticker_id='2')
        line_bot_api.reply_message(
        event.reply_token,sticker)

    elif msg in ['Hi', 'hi']:
        reply_text = 'Yo'
    elif msg in ['你好','哩賀']:
        reply_text = '哩賀'
    else:
        reply_text = '聽不懂R'
        sticker = StickerSendMessage(
        package_id='1',
        sticker_id='2')

#line 一次只能回傳一個訊息，所以如果要兩個都貼要用list!!!!

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(reply_text), sticker])
   

    
#一條一條寫在裡面叫做rule based, 人工智慧通常不是
#Ai NLP natural language processing
#通常會把code寫成main function，寫下面這行是希望直接讀取才執行
#避免import app.py的時候就開始跑
if __name__ == "__main__": 
    app.run(debug = True)
