# 全体の流れ
# ①コードを書く("Talk API"とLINEDeveloperの"Channel secret"を取得してから)
# ②ローカルリポジトリを作成する
# ③Githubのリモートリポジトリにローカルリポジトリを送る
# ④HerokuとGithubを連携する
# ⑤LINE DeveloperのWebhookにHerokuのデプロイしたURLを貼り付ける
# ⑥URLにデコレータの”/callback”を追記する

from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import pya3rt
import os

app=Flask(__name__)


linebot_api=LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])

handler=WebhookHandler(os.environ['CHANNEL_SECRET'])

@app.route("/callback",methods=['POST'])
def callback():
    signature=request.headers["X-Line-Signature"]
    body=request.get_data(as_text=True)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    ai_message=talk(event.message.text)
    linebot_api.reply_message(event.reply_token,TextSendMessage(text=ai_message))

@handler.add(FollowEvent)
def handle_follow(event):
    linebot_api.reply_message(event.reply_token,TextSendMessage(text=
        'はじめまして！登録ありがとうございます！こちらはAIと気軽に話せるチャンネルとなっております。何か話しかけてみてください！'
    ))

def talk(call):
    apikey=os.environ['TALK_API']
    client=pya3rt.TalkClient(apikey)
    reply=client.talk(call)
    return reply['results'][0]['reply']

if __name__=='__main__':
    app.run()

