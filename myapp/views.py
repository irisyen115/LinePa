import logging
from os import getcwd
from django.shortcuts import render
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
                    data=Song.objects.all()
                    logger.error(data.count())
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

def is_num(n):
  is_number = True
  try:
    num = float(n)
    # 檢查 "nan" 
    is_number = num == num  # 或者使用 `math.isnan(num)`
  except ValueError:
    is_number = False
  return is_number

