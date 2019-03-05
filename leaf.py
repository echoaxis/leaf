# Author:   Greg Smith
# Version:  0.1 2018
# leaf

# this code draws upon and was inspired by both http://dreamingecho.es/internet-of-things-with-python-and-flask/ and
# the book 'Getting Started with Raspberry Pi (Make: Projects) by Matt Richardson' weblamp project https://www.amazon.com/dp/1449344216/ref=cm_sw_r_tw_dp_U_x_d1K7Bb8MX44TG


#import time, datetime
import Adafruit_DHT as dht
from flask import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

app = Flask(__name__)

#Create a dictionary for togglePins, store the gpio, description, and state:
togglePins = {
   16: {'zone' : 16, 'name' : 'Back Lawn', 'state' : GPIO.LOW},
   20 : {'zone' : 20, 'name' : 'Back Hedge', 'state' : GPIO.LOW},
   21: {'zone' : 21, 'name' : 'Vegie Garden', 'state' : GPIO.LOW},
   19 : {'zone' : 19, 'name' : 'Side Hedge', 'state' : GPIO.LOW},
   26 : {'zone' : 26, 'name' : 'Courtyard', 'state' : GPIO.LOW}
}
dht11pin = 18

# Set each pin as an output and make it low:
for togglePin in togglePins:
   GPIO.setup(togglePin, GPIO.OUT)
   GPIO.output(togglePin, GPIO.LOW)

# Default route
@app.route("/")
def main():
  # Render the about.html template
  return render_template('index.html')

#zone route
@app.route("/zone")
@app.route("/zones")
def io():
    # For each pin, read the pin state and store it in the pins dictionary:
    for togglePin in togglePins:
        togglePins[togglePin]['state'] = GPIO.input(togglePin)
    # Put the pin dictionary into the template data dictionary:
    pinData = {
        'togglePins' : togglePins
      }
    # Pass the template data into the template and return it to the user
    return render_template('zone.html', **pinData)

# weather route
@app.route("/weather")
def weather():
    # Read DHT 11 data and store the data
    humidity, temperature = dht.read_retry(dht.DHT11, dht11pin)
    tempData = {'humidity': humidity, 'temperature': temperature}
    # Pass the template data into the template and return it to the user
    return render_template('weather.html', **tempData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/zone/<changePin>/<action>")
@app.route("/zones/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = togglePins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned the " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned the " + deviceName + " off."
   if action == "toggle":
      # Read the pin and set it to whatever it isn't (that is, toggle it):
      GPIO.output(changePin, not GPIO.input(changePin))
      message = "Toggled " + deviceName + "."

   # For each pin, read the pin state and store it in the togglePin dictionary:
   for togglePin in togglePins:
      togglePins[togglePin]['state'] = GPIO.input(togglePin)

   # Along with the togglePin dictionary, put the message into the template data dictionary:
   pinData = {
      'message' : message,
      'togglePins' : togglePins
   }
   return render_template('zone.html', **pinData)

# schedule route
@app.route("/schedule")
def schedule():
  return render_template('soon.html')

# statistics route
@app.route("/statistics")
def statistics():
  return render_template('soon.html')

# settings route
@app.route("/settings")
def settings():
  return render_template('soon.html')

# todo route
@app.route("/todo")
def todo():
  return render_template('todo.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)