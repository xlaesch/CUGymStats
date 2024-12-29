import requests
from fake_useragent import UserAgent

#TODO: add user-agent header to bypass mod_security
r = requests.get("https://connect2concepts.com/connect2/?type=circle&key=355de24d-d0e4-4262-ae97-bc0c78b92839&loc_status=false")

print(r) #gives status code of response received

print(r.content)


ua = UserAgent()
print(ua.random)