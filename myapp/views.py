import logging
from os import getcwd
from django.shortcuts import render
from datetime import datetime
from .models import Song
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, StickerSendMessage, FlexSendMessage
from myapp.models import Song
from django.http import JsonResponse
import logging
import json
logger = logging.getLogger('django.server')


# Create your views here.
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    reply = "無法辨識"    
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
               
        for event in events:
            if isinstance(event, MessageEvent):
                msg = event.message.text
                try:
                    records = Song.objects.filter(song_name__contains=msg)  
                    c = records.count()
                    if 0 < c <= 12:
                        reply = flex_message(records,msg)
                    elif c > 12:
                        logger.error("Hello")
                        reply = limit_bubble(c,msg)
                        logger.error("Hello")
                    else:
                        reply = StickerSendMessage(package_id=11538,sticker_id=51626497);
                except Exception as e:
                    logger.error(e + "cd")
                try:
                    logger.error("before")
                    line_bot_api.reply_message(event.reply_token, reply)
                    logger.error("after")
                except Exception as e:
                    logger.error ("長度"+records.count())

        return HttpResponse()
    else:
        return HttpResponseBadRequest("Avengers assemble")

def flex_message(records,msg):
    bubbles = []
    for rec in records:
        bubble = make_bubble(rec)
        bubbles.append(bubble)

    carousel = {
        "type": "carousel",
        "contents": bubbles
    }
    return FlexSendMessage(contents=carousel, alt_text=msg)

def limit_bubble(c,msg):
    content_json={
    "type": "bubble",
    "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "請再輸入更詳細的關鍵字",
            "margin": "lg",
            "size": "lg",
            "weight": "bold"
        }
        ]
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "hello, world",
            "contents": [
            {
                "type": "span",
                "text": "關鍵字"
            },
            {
                "type": "span",
                "text": msg,
                "color": "#FF0000",
                "size": "3xl"
            },
            {
                "type": "span",
                "text": "有包含"
            },
            {
                "type": "span",
                "text": str(c),
                "color": "#FF0000",
                "size": "3xl"
            },
            {
                "type": "span",
                "text": "個結果"
            }
            ],
            "margin": "xxl",
            "size": "lg",
            "weight": "bold"
        }
        ]
    }
    }
    return FlexSendMessage(contents=content_json,alt_text=msg)

def make_bubble(rec):
    return {"type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": rec.song_name,
                "margin": "lg",
                "size": "lg",
                "weight": "bold"
            }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "weight": "bold",
                "size": "3xl",
                "text": rec.song_num
            }
            ],
            "alignItems": "center"
        }
    }    
    

@csrf_exempt
def song_page(request):
    return render(request, 'songpage.html')

@csrf_exempt
def create(request):
    logger.error("Hello")
    data = json.loads(request.body.decode('utf-8'))
    songname = data['songname']
    songnum = data['songnum']
    records = Song.objects.filter(song_name=songname)
    if records.count() > 0:
        return HttpResponse(status=500)        
    elif songnum.isdigit() == False:
        return HttpResponse(status=500)
    else:
        Song.objects.create(song_name = songname,song_num = songnum)
        return HttpResponse(status=200)        
@csrf_exempt
def song_list(request):
    song_list = Song.objects.all()
    return render(request, 'songlist.html', {
        'song_list': song_list,
        'song.song_name':(x.song_name for x in song_list),
        'song.song_num':(y.song_num for y in song_list)
    })
@csrf_exempt
def delete(request):
    data = json.loads(request.body.decode('utf-8'))
    songid = data['id']
    data_2 = Song.objects.filter(id = songid)
    data_2.delete()
    return HttpResponse()
