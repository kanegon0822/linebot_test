# -*- coding: utf-8 -*-
"""LINEbot練習.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12PXOozQ6ahIh9y88jivA2XB9EGPmrvp9
"""


from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import pya3rt

app=Flask(__name__)


linebot_api=LineBotApi('K1QBI9rW4/d5oRv/VgQNq6rhv35yetVbqOByp89cuE4Y7uWpgz/3xI/U6iSebWNp1a8Kedau83VuLjtktJ0LCh65wm7wsnDJeRF8MTfpRUHOHVsKt/fair5ox5uC8m8/k8KgIn+SiqF3M18voR8+wAdB04t89/1O/w1cDnyilFU=')

handler=WebhookHandler('acc5a1d6605c928b8a83ee084a26d9d6')

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


def talk(call):
    apikey="DZZeqgnJIzeGIsw8UxnAAfog2qp8B6Qm"
    client=pya3rt.TalkClient(apikey)
    reply=client.talk(call)
    return reply['results'][0]['reply']

if __name__=='__main__':
    app.run()
