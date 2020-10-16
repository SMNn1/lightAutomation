import requests


url = 'http://192.168.2.185/api/RAinKmADdhVuOV--GVyptV-u4QaxpNaVGBG5N1cr/lights/30/state'
payload = {'on': False}

r = requests.put(url, json = payload, timeout=1)

print(r.text)

