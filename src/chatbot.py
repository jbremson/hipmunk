from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import re
from src.secrets import GMAPS_KEY, DARK_SKY_KEY
import time
import urllib.request

app = Flask(__name__)
CORS(app)

class ResponseManager():
    """Compose, validate, and return response sets."""

    def __init__(self):
        self.responses = []

    def add_response(self, type, text):
        """Add a response to the response set. Valid types are 'text' and 'rich'
        """
        if type not in ['text', 'rich']:
            return self.invalid_response("Invalid response type: {}".format(type))
        self.responses.append(dict(type=type, text=text))

    def return_response_json(self):
        """Return a json string of the response set. """
        return json.dumps(dict(messages=self.responses))

def invalid_response(message):
    """Return an invalid response message as json."""
    response_manager = ResponseManager()
    message = "ERROR: " + message
    response_manager.add_response(type='text', text=message)
    return response_manager.return_response_json()

def get_url(url, attempts=3, sleep=0.3, debug=False):
    """Return content of <url>, making <attempts>, with time <sleep> between attempts. """
    tries = 0
    while tries < attempts:
        try:
            with urllib.request.urlopen(url) as url_reader:
                return url_reader.read()
        except Exception as e:
            if debug:
                print("Failed: Attempt {} - {}".format(tries, e))
            tries += 1
            time.sleep(sleep)
    return invalid_response("Unable to access url: {}".format(url))

def geolocate(address):
    """Return a {'lat':...,'lng':...} dict for the given address."""
    address = re.sub("[, ]+","+", address)
    url = "https:// maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, GMAPS_KEY)
    return json.loads(get_url(url))['results'][0]['geometry']['location']

def weather(loc):
    """Gets the weather given dict {'lat':..., 'lng':...}. """
    url = "https://api.darksky.net/forecast/{}/{},{}?" \
          "exclude=minutely,hourly,daily,alerts,flags".format(DARK_SKY_KEY, loc['lat'], loc['lng'])
    weather_info = json.loads(get_url(url))['currently']
    return dict(summary=weather_info['summary'], temperature=weather_info['temperature'])

def get_weather(text):
    """Returns weather info. Input <text> is input string like 'Get weather in San Francisco'."""
    # Remove extra white space and upper case from text
    text = re.sub("[ ]+", " ", text.strip().lower())
    location = None
    # Simple algorithm here. Split the text on 'weather in'. If we find it take the right side.
    # If we don't find it split on 'weather' and take the left side for location.
    # If we don't find a location throw an invalid response screen.
    tokens = text.split("weather in")
    if len(tokens)==2:
        location = tokens[1]
    if not location:
        tokens = text.split("weather")
        if len(tokens) == 2:
            location = tokens[0]
    if not location:
        return invalid_response("I do not understand '{}'".format(text))
    return weather(geolocate(location))







@app.route('/chat/messages', methods=['POST'])
def message():
    if request.method == 'POST':
        response_manager = ResponseManager()
        vals = json.loads(json.dumps(request.form))
        if vals['action'] == 'join':
            if not vals.get("user_id") and not vals.get("name"):
                return invalid_response("'user_id' and/or 'name key is missing.")
            response_manager.add_response('text', "Hello {}!". format(vals['name'].capitalize()))
        elif vals['action'] == 'message':
            weather_data = get_weather(vals['text'])
            response_manager.add_response('text', "Currently it's {}F. {}.".format(weather_data['temperature'],
                                                                                   weather_data['summary']))
        else:
            return invalid_response("No valid 'action' key in request.")
        return response_manager.return_response_json()


