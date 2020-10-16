import requests, json


baseurl = 'http://192.168.2.19/api/RAinKmADdhVuOV--GVyptV-u4QaxpNaVGBG5N1cr/lights'



addedurl = '/30/state'


# r = requests.put(baseurl + addedurl, json = payload, timeout=1)

# print(r.text)

def turnOnRoom(lightName):
    return "tesd"

def getListOfLights():
    result = requests.get(baseurl, timeout=1)
    return result.json()

lights = getListOfLights()

def turnOnLight(lightName):
    for light in lights:
        if lights[light]['name'] == lightName:
            payload = {'on': True}
            r = requests.put(baseurl + '/' + light + '/state', json = payload, timeout=1)
            print(r)




# print(lights['22']['name'])

turnOnLight('Playroom Decke Kugel')


