from django.shortcuts import render

from ttd.models import *
import os
from pathlib import Path

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def homepage(request):
    return render(request, 'healthdiary.html')


@csrf_exempt
def pic(request):
    return render(request, 'surprise.html')

@csrf_exempt
def showalluser(request):
    names = ''
    for i in User_Info.objects.all():
        #myname += str(i) + '<br>'
        names += i.username + '<br>'
    return HttpResponse(names)

@csrf_exempt
def test(request):
    names=''
    f=open('food.txt')
    foodlist=f.readline()
    names += foodlist + '<br>'
    return HttpResponse(names)




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
                if event.message.type=='text':
                    mtext=event.message.text
                    uid=event.source.user_id
                    profile=line_bot_api.get_profile(uid)
                    name=profile.display_name
                    pic_url=profile.picture_url
                    message=[]

                    seqnum = 0 
                    mes=event.message.text.split(" ")
                    for s in range(len(event.message.text)):
                        if event.message.text[s] == " ":
                            seqnum = seqnum + 1
                    seqnum = seqnum + 1
                    '''message.append(TextSendMessage(text=mes[0]))
                    line_bot_api.reply_message(event.reply_token,message)'''

                    if mes[0] == '??????????????????':
                        if User_Info.objects.filter(uid=uid).exists()==False:
                            User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext)
                            message.append(TextSendMessage(text='????????????????????????'))
                        elif User_Info.objects.filter(uid=uid).exists()==True:
                            message.append(TextSendMessage(text='??????????????????????????????'))
                            user_info = User_Info.objects.filter(uid=uid)
                            for user in user_info:
                                info = 'UID=%s\nNAME=%s\n?????????=%s'%(user.uid,user.name,user.pic_url)
                                message.append(TextSendMessage(text=info))
                        line_bot_api.reply_message(event.reply_token,message)
                    elif mes[0] == '?????????':
                        message.append(TextSendMessage(text='????????????'))
                        line_bot_api.reply_message(event.reply_token,message)
                    elif mes[0] == '??????jk????????????' :
                        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://spacetotest.herokuapp.com/static/kai.jpg', preview_image_url='https://spacetotest.herokuapp.com/static/kai.jpg'))

                    elif mes[0] == '????????????':
                        message.append(TextSendMessage(text='????????????????????????bmi'))
                        message.append(TextSendMessage(text='????????????????????????[????????? ?????? ?????? ??????]????????????'))
                        message.append(TextSendMessage(text='?????????bmi?????????[bmi ?????? ??????]????????????'))
                        message.append(TextSendMessage(text='???????????????thehealthdiary.herokuapp.com'))
                        line_bot_api.reply_message(event.reply_token,message)

                    elif mes[0] == '?????????' :
                        f=open('%s/food.txt' %BASE_DIR)
                        foodlist=f.readlines()
                        cal = 0
                        for n in range(1,seqnum):
                            for i in range(132):
                                if mes[n] == foodlist[i].replace("\n",""):
                                    cal = cal + int(foodlist[i+1].replace("\n",""))
                        message.append(TextSendMessage(text='%s cal' %cal))
                        line_bot_api.reply_message(event.reply_token,message)
                        f.close()
                    
                    elif mes[0] == 'bmi':
                        highth=float(mes[1])/100
                        weight=float(mes[2])
                        bmi=float(weight/(highth * highth))
                        message.append(TextSendMessage(text='your bmi = %.2f' %bmi))
                        line_bot_api.reply_message(event.reply_token,message)


        return HttpResponse()
    else:
        return HttpResponseBadRequest()