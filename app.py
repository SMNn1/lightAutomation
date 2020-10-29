from flask import Flask, render_template, request, redirect
from datetime import date
import requests, json, random, time
import mysql.connector

app = Flask(__name__)

@app.route('/')
def hello():
    return redirect("/index", code=302)

@app.route('/index', methods = ['POST', 'GET'])
def index():
    action = request.args.get('action')
    lightId = request.args.get('id')
    if action == 'switch':
        switchHueLightId(lightId)
    elif action == 'colorfade':
        allowExtraMode = True
        fadingColorsId(lightId)
    elif action == 'partymode':
        allowExtraMode = True
        partymode(lightId)
    elif action == 'stop':
        allowExtraMode = False
    return render_template('index.html', dateNow = getCurrentDate(), lightsData = getLightsData())

baseurl = 'http://192.168.2.19/api/RAinKmADdhVuOV--GVyptV-u4QaxpNaVGBG5N1cr/'

def getListOfHueLights():
    result = requests.get(baseurl + 'lights', timeout=1)
    return result.json()

def switchHueLight(lightName, state):
    lights = getListOfHueLights()
    for light in lights:
        if lights[light]['name'] == lightName:
            payload = {'on': state}
            requests.put(baseurl + 'lights/' + light + '/state', json = payload, timeout=1)

def switchHueLightId(lightId):
    stateOn = getListOfHueLights()[lightId]['state']['on']
    if stateOn == True:
        targetStateOn = False
    elif stateOn == False:
        targetStateOn = True
    payload = {'on': targetStateOn}
    requests.put(baseurl + 'lights/' + lightId + '/state', json = payload, timeout=1)

def getListOfHueGroups():
    groupsDict = {}
    result = requests.get(baseurl + 'groups', timeout=1)
    groups = result.json()
    for groupNr in groups:
        groupsDict[groupNr] = groups[groupNr]['name']
    return groupsDict

def getLightsOfHueGroup(groupName):
    result = requests.get(baseurl + 'groups', timeout=1)
    groups = result.json()
    for groupNr in groups:
        if groups[groupNr]['name'] == groupName:
            lightsArray = groups[groupNr]['lights']
    return lightsArray

def switchHueGroup(groupName, state):
    result = requests.get(baseurl + 'groups', timeout=1)
    groups = result.json()
    for groupNr in groups:
        if groups[groupNr]['name'] == groupName:
            payload = {'on': state}
            requests.put(baseurl + 'groups/' + groupNr + '/action', json = payload, timeout=1)

def switchRandomColor(lightName):
    colorCode = random.randint(0,65535)
    lights = getListOfHueLights()
    for lightNr in lights:
        if lights[lightNr]['name'] == lightName:
            payload = {
                'hue': colorCode,
                'sat': 254,
                'bri': 254
            }
            requests.put(baseurl + 'lights/' + lightNr + '/state', json = payload, timeout=1)
            return colorCode

def switchRandomColorId(lightId):
    colorCode = random.randint(0,65535)
    lights = getListOfHueLights()
    payload = {
        'hue': colorCode,
        'sat': 254,
        'bri': 254
    }
    requests.put(baseurl + 'lights/' + lightId + '/state', json = payload, timeout=1)
    return colorCode

def partymode(lightId):
    while allowExtraMode:
        print(switchRandomColorId(lightId))
        time.sleep(0.5)

def fadingColors(lightName):
    lights = getListOfHueLights()
    for light in lights:
        if lights[light]['name'] == lightName:
            colorCode = lights[light]['state']['hue']
            while True:
                colorCode = incrementColorCode(colorCode, 2)
                payload = {
                    'hue': colorCode,
                    'sat': 254,
                    'bri': 254
                }
                requests.put(baseurl + 'lights/' + light + '/state', json = payload, timeout=1)
                time.sleep(0.5)

allowExtraMode = True

def fadingColorsId(lightId):
    global allowExtraMode
    lights = getListOfHueLights()
    colorCode = lights[lightId]['state']['hue']
    while allowExtraMode:
        colorCode = incrementColorCode(colorCode, 1)
        payload = {
            'hue': colorCode,
            'sat': 254,
            'bri': 254
        }
        requests.put(baseurl + 'lights/' + lightId + '/state', json = payload, timeout=1)
        time.sleep(0.2)

def incrementColorCode(colorCode, speed):
    increAmount = random.randint(500,1000) * speed
    if (colorCode + 600) > 65535:
        colorCode = 0
    colorCode = colorCode + increAmount
    return colorCode

def getCurrentDate():
    dateNow = date.today().strftime("%Y-%m-%d")
    return dateNow

def getLightsData():
    lights = getListOfHueLights()
    resArray = []
    for light in lights:
        lightName = lights[light]['name']
        lightState = lights[light]['state']
        lightStateOn = lights[light]['state']['on']
        if "hue" in lightState:
            lightStateHue = lights[light]['state']['hue']
        else:
            lightStateHue = -1
        light = {
            'id': light,
            'name': lightName,
            'on': lightStateOn,
            'hue': lightStateHue,
        }
        resArray.append(light)
    return resArray

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')