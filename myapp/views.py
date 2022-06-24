from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage


# Create your views here.
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
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
                if is_num(msg):
                    msg = float(msg)*2			
                elif "xd" in msg:
                    msg = "笑什麼笑"
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))

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
