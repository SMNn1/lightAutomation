from reptimer import RepeatedTimer
import requests, json, random, time


baseurl = 'http://192.168.2.19/api/RAinKmADdhVuOV--GVyptV-u4QaxpNaVGBG5N1cr/'



# r = requests.put(baseurl + addedurl, json = payload, timeout=1)

# print(r.text)

def getListOfHueLights():
    result = requests.get(baseurl + 'lights', timeout=1)
    return result.json()

def switchHueLight(lightName, state):
    lights = getListOfHueLights()
    for light in lights:
        if lights[light]['name'] == lightName:
            payload = {'on': state}
            requests.put(baseurl + 'lights/' + light + '/state', json = payload, timeout=1)

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

def fadingColors(lightName):
    lights = getListOfHueLights()
    for light in lights:
        if lights[light]['name'] == lightName:
            colorCode = lights[light]['state']['hue']
            while True:
                colorCode = incrementColorCode(colorCode, 1)
                payload = {
                    'hue': colorCode,
                    'sat': 254,
                    'bri': 254
                }
                requests.put(baseurl + 'lights/' + light + '/state', json = payload, timeout=1)
                time.sleep(0.2)

def incrementColorCode(colorCode, speed):
    increAmount = random.randint(500,1000) * speed
    if (colorCode + 600) > 65535:
        colorCode = 0
    colorCode = colorCode + increAmount
    return colorCode

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
            'name': lightName,
            'on': lightStateOn,
            'hue': lightStateHue,
        }
        resArray.append(light)
    return resArray

# fadingColors('Schlafzimmer Decke Blume')



# while True:
#     print(switchRandomColor('Bad Decke'))
#     time.sleep(0.5)

# payload = {
#     'hue': 20000,
#     'sat': 254,
#     'bri': 254
# }
# r = requests.put(baseurl + 'lights/30/state', json = payload, timeout=1)
# print(r)

results = getLightsData()
for res in results:
    print(res['name'])


# name, type, state, color
