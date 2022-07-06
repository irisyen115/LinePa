import logging
from os import getcwd
from django.shortcuts import render
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from myapp.models import Song
import logging
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
                    records = Song.objects.filter(song_name=msg)
                    if 0 < records.count():
                        reply=records[0].song_num
                    else:
                        reply = "我大意了沒有閃"
                except Exception as e:
                    logger.error(e)

                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

        return HttpResponse()
    else:
        return HttpResponseBadRequest("Avengers assemble")

@csrf_exempt
def song_page(request):
    return render(request, 'songpage.html')

@csrf_exempt
def create(request):
    if request.method == 'POST':
        songname= request.POST["song_name"]
        songnum = request.POST["song_num"]
    records = Song.objects.filter(song_name=songname)
    if records.count() > 0:
        reason = "歌名已儲存"
        return render(request, 'create_fail.html',{
        'current_time': str(datetime.now()),
        'song_name': songname,
        'song_num': songnum,
        'reason':reason
    })
    if songnum.isdigit():
        Song.objects.create(song_name = songname,song_num = songnum)
        return render(request, 'create_success.html',{
        'current_time': str(datetime.now()),
        'song_name': songname,
        'song_num': songnum   
    })
    else:
        reason = "無法辨識歌號"
        return render(request, 'create_fail.html',{
        'current_time': str(datetime.now()),
        'song_name': songname,
        'song_num': songnum,
        'reason': reason
    })
