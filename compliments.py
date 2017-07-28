import json, random, requests, re, time
import config
from flask import Flask
from flask_mail import Mail, Message
app = Flask(__name__)
mail=Mail(app)

app.config.update(
        DEBUG=True,
        #EMAIL SETTINGS
        MAIL_SERVER='sslout.df.eu',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME = 'compliments@wikimedia.de',
        MAIL_PASSWORD = config.password
        )

mail=Mail(app)
#addresses = ['jens.ohlig@wikimedia.de', 'charlie.kritschmar@wikimedia.de']

@app.route("/")
def compliment():
    r = requests.get("https://www.wikimedia.de/wiki/Mitarbeitende")
    addresses = list(set(re.findall(r'\w+\.\w+@wikimedia.de', r.text)))

    # Special thanks to fundraising
    date = (time.strftime("%d/%m/%Y"))
    if (date == '12/01/2017'): 
	addresses = ['till.mletzko@wikimedia.de', 'tobias.schumann@wikimedia.de', 'carsten.direske@wikimedia.de', 'wladimir.raizberg@wikimedia.de', 'mia.buller@wikimedia.de', 'hannah.weber@wikimedia.de', 'solveigh.mertins@wikimedia.de']

    address = [random.choice(addresses)]
    with open('compliments.json') as json_data:
            compliments = json.load(json_data)

    msg = Message(
          'Someone pressed the compliment button! Here is a compliment for you!',
          sender='compliments@wikimedia.de',
          recipients = address
    )
    msg.body = random.choice(compliments)
    mail.send(msg)
    return "You are awesome!"

if __name__ == "__main__":
    app.run()
