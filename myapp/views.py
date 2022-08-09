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
from linebot.models import MessageEvent, TextSendMessage, StickerSendMessage
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
                    logger.error("Hello")
                    records = Song.objects.filter(song_name__contains=msg)
                    if 0 < records.count():
                        reply = TextSendMessage(text=records[0].song_num)
                    else:
                        reply = StickerSendMessage(package_id=11538,sticker_id=51626497);
                except Exception as e:
                    logger.error(e)
                    
                logger.error("Hello")
                line_bot_api.reply_message(event.reply_token, reply)

        return HttpResponse()
    else:
        return HttpResponseBadRequest("Avengers assemble")

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
