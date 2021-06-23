import requests

url = 'http://192.168.1.50:8090/cars'

def get_cars():
    x = requests.get(url)

    print(x.text)


def get_car(n):    
    x = requests.get(f"{url}/{n}")

    print(x.text)

def add_car(json):
    x = requests.post(url, json=json)    

    print(x.text)


def delete_car(n):
    x = requests.delete(f"{url}/{n}")

    print(x.text)


json = {
    "brand" : "Test",
    "model" : "Test",
    "year" : 2021,
    "description" : "YEP"
    }
#add_car(json)    
#get_car(7)
#delete_car(9)