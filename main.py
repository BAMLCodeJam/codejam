#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask import render_template
from flask import request
from api import *

template_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__,
            template_folder=template_dir,
            static_url_path='',
            static_folder=template_dir)
import json
from watson_developer_cloud import ConversationV1

CONVERSATION = ConversationV1(
        username='7859a24d-768c-46f3-bf57-d13a8a61b975',
        password='3X4GfI4qnbOB',
        version='2017-10-01')
WORKSPACE_ID = '27511189-bce7-48ad-85b9-ff79b5d9d4ff'

    
@app.route("/")
def index():
    print 'INDEX'
    return render_template("index.html")

@app.route("/<name>")
def hello(name):
    return render_template("index.html",name=name.title())

@app.route("/signup", methods=['POST'])
def sign_up():
    form_data = request.form
    name = form_data['name']
    print name
    print form_data['email']
    return render_template("signup.html",name=name.title())


@app.route("/email", methods=['POST'])
def email():
    form_data = request.form
    emails = [e.strip() for e in form_data['emailinput'].split(',')]
    print emails
    subject = "Hello Maria"
    msg = "Congratulations Maria, you just sent an email with Mailgun!  You are truly awesome!  " \
            "You can send up to 300 emails/day from this sandbox server. "
    m = Mailgun()
    result = m.send(emails,subject,msg)
    return render_template("index.html", email=result.status_code)


@app.route("/weather", methods=['POST'])
def weather():
    w = Weather()
    form_data = request.form
    name = form_data['city']
    result = w.weatherByCity(name).json()
    print result
    temp = result['main']['temp']
    city = result['name']
    country = result['sys']['country']
    weather = result['weather'][0]['main']
    print temp, city, country, weather
    msg = u"It's {}ºC in {} {}, and the sky is {} ".format(temp, city, country, weather)
    return render_template("index.html", weather=msg)

@app.route("/tweets", methods=['POST'])
def twitter():
    t = Twitter()
    form_data = request.form
    tag = form_data['tag']
    result = t.getTweetsForTag(tag)
    tweets = []
    for tweet in result:
        tweets.append(u"{} - {}".format(tweet.user.name,tweet.text))
    return render_template("index.html", tweets=tweets)


@app.route("/foursquare", methods=['POST'])
def foursquare():
    f = Foursquare()
    form_data = request.form
    location = form_data['location']
    result = f.exploreVenues(location).json()
    venues = []
    for item in result['response']['groups'][0]['items']:
        name = item['venue']['name']
        rating = item['venue']['rating']
        address = ", ".join(item['venue']['location']['formattedAddress'])
        venues.append(u"Name: {}, Rating: {}, Address: {}".format(name, rating, address))
    return render_template("index.html", venues=venues)

@app.route("/uber", methods=['POST'])
def uber_product():
    u = UberRides()
    form_data = request.form
    latitude = form_data['latitude']
    longitude = form_data['longitude']
    products = u.getProducts(latitude, longitude)
    return render_template("uberPage.html", products=products)

@app.route("/aftership", methods=['POST'])
def aftership_Create_Shipment():
    a = AfterShip()
    form_data = request.form
    slug = form_data['slug']
    number = form_data['number']
    title = form_data['title']
    ShipmentInfo = a.createShipment(slug,number,title)
    return render_template("index.html", ShipmentInfo=ShipmentInfo)


def speak(message, context):
    result = CONVERSATION.message(workspace_id=WORKSPACE_ID, message_input={'text': message}, context=context)
    return result['output']['text'][0], result['context']


@app.route("/watson", methods=['POST'])
def conversation():
    form_data = request.form
    message = form_data.get('answer', '')
    try:
        context = json.loads(form_data.get('context', "{}"))
    except ValueError:
        # No context yet, we create it empty
        context = {}
    response, context = speak(message, context)
    return render_template("watson.html", response=response, context=json.dumps(context))


#app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
if __name__ == "__main__":
    app.run(port=65438)