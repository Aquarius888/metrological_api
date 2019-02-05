import grequests
import requests

session = requests.Session()

def exception_handler(request, exception):
    print("Request failed", request.url)
    print(str(exception))


with open("C:\\Users\\Pavel_Alekseev\\Desktop\\desktop\\test\\urls.txt") as werewolves:
    array = ['https://' + row.strip() for row in werewolves]

rs = [grequests.get(u) for u in array]
print(rs)
for r in grequests.map(rs, size=16, exception_handler=exception_handler):
    #print(r)
    print(r.status_code, r.url, r.headers)
