#!/usr/bin/env python3

import json
import random
import requests
import re
import time
import config
from flask import Flask, Markup
from flask_mail import Mail, Message
from bs4 import BeautifulSoup
app = Flask(__name__)
mail = Mail(app)

app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='sslout.df.eu',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='compliments@wikimedia.de',
    MAIL_PASSWORD=config.password,
    MAIL_SUPPRESS_SEND=hasattr(
        config, 'suppress_send') and config.suppress_send
)

mail = Mail(app)

wpLoginTokenPattern = re.compile('<input type="hidden" name="wpLoginToken" value="([^"]*)" />')


def loadCompliments():
    wpLoginTokenRequest = requests.get(
        config.wikiurl,
        params = {
            'title': 'Special:Login'
        }
    )
    wpLoginToken = re.search(wpLoginTokenPattern, wpLoginTokenRequest.text).group(1)

    complimentsRequest = requests.post(
        config.wikiurl,
        cookies=wpLoginTokenRequest.cookies,
        data = {
            'title': 'Special:Login',
            'action': 'submitlogin',
            'type': 'login',
            'returnto': config.complimentspage,
            'wpName': config.wikiuser,
            'wpPassword': config.wikipassword,
            'wpDomain': config.wikidomain,
            'wpLoginToken': wpLoginToken
        }
    )

    soup = BeautifulSoup(complimentsRequest.text, 'html.parser')
    content = soup.find('div', { 'id': 'mw-content-text' })
    complimentListItems = content.findAll('li')
    compliments = [complimentListItem.string.strip() for complimentListItem in complimentListItems]

    return compliments


@app.route("/")
def compliment():
    r = requests.get("https://www.wikimedia.de/wiki/Mitarbeitende")
    addresses = list(set(re.findall(r'\w+\.\w+@wikimedia.de', r.text)))

    address = [random.choice(addresses)]
    compliments = loadCompliments()

    msg = Message(
        'Someone pressed the compliment button! Here is a compliment for you!',
        sender=app.config['MAIL_USERNAME'],
        recipients=address
    )
    msg.body = random.choice(compliments)
    mail.send(msg)

    markup = Markup('<!DOCTYPE html><html>')
    markup += Markup('<head><meta charset="utf-8"><title>You are awesome!</title></head>')
    markup += Markup('<body><pre>')
    markup += Markup.escape(msg.as_string())
    markup += Markup('</pre></body>')
    markup += Markup('</html>')
    return markup


if __name__ == "__main__":
    app.run()
