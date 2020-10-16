import requests, json


baseurl = 'http://192.168.2.19/api/RAinKmADdhVuOV--GVyptV-u4QaxpNaVGBG5N1cr/'





# r = requests.put(baseurl + addedurl, json = payload, timeout=1)

# print(r.text)

def turnOnRoom(lightName):
    return "tesd"

def getListOfHueLights():
    result = requests.get(baseurl + 'lights', timeout=1)
    return result.json()

def turnOnHueLight(lightName):
    lights = getListOfHueLights()
    for light in lights:
        if lights[light]['name'] == lightName:
            payload = {'on': True}
            r = requests.put(baseurl + 'lights/' + light + '/state', json = payload, timeout=1)
            print(r)

def getListOfHueGroups():
    groupsDict = {}
    result = requests.get(baseurl + 'groups', timeout=1)
    groups = result.json()
    for groupNr in groups:
        groupsDict[groupNr] = groups[groupNr]['name']
    return groupsDict

# turnOnHueLight('Playroom Decke Kugel')

print(str(getListOfHueGroups()))