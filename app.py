from flask import Flask, request
import requests
from pexels_api import API
from twilio.twiml.messaging_response import MessagingResponse
from random import randrange
import os
import boto3

app = Flask(__name__)

PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')
api = API(PEXELS_API_KEY)


@app.route('/bot', methods=['GET','POST'])
def bot():
    search_param = request.values.get('Body', '').lower()
    image_attached = False

    api.search(search_param, page=1, results_per_page=100)
    photos = api.get_entries()
    resp = MessagingResponse()
    msg = resp.message()
    try:
        image = photos[(randrange(39))].medium
        msg.media(image)
        image_attached = True
    except IndexError:
        print('no image meets that description')
    except:
        print('an unknown error has occured')


    # add text body
    r = requests.get('https://api.quotable.io/random')
    if not image_attached:
        quote = 'Sorry, I could not find an image with that description ¯\_(ツ)_/¯.'
    elif r.status_code == 200:
        data = r.json()
        quote = f'{data["content"]} --{data["author"]}'
    else:
        quote = 'no quote today, sorry'
    msg.body(quote)

    return str(resp)


@app.route('/justacat', methods=['POST'])
def justacat():
    incoming_msg = request.values.get('Body', '').lower()
    print(incoming_msg)

    # twilio parts
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} --{data["author"]}'
        else:
            quote = 'no quote today, sorry'
        msg.body(quote)
        responded = True

    if 'cat' in incoming_msg:
        msg.media('https://cataas.com/cat')
        responded = True

    if not responded:
        msg.body('I only know about famous quotes and cats, sorry.')
    return str(resp)


# tik-tok videos
@app.route('/tok', methods=['POST'])
def tok():
    resp = MessagingResponse()
    msg = resp.message()
    msg.media('https://v39-us.tiktokcdn.com/ec366a3fc060c986534e7c327ec677f3/60529b1a/video/tos/useast2a/tos-useast2a-ve-0068c003/bbd1943fab8a4dd49cc20f544cca82f2/?a=1233&br=2590&bt=1295&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&l=20210317181303010190209088582F73D7&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&qs=0&rc=MzdwaDV1c3FuNDMzaDczM0ApOmQ0M2Y4ZmRpNzZmZThpOmdwcHFsbDYwZzFgLS0wMTZzc14xX2IwYC5iYC1jMWJfMC46Yw%3D%3D&vl=&vr=')
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)