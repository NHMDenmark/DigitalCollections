import requests
from getpass import getpass


baseURL = 'https://specify-snm.science.ku.dk/'



# Create a session for storing cookies 
sess = requests.Session() 


# Prepare login
response = sess.get(baseURL + "context/login/")
csrftoken = response.cookies.get('csrftoken')
cookies = response.cookies
print(response.request)
#print(response.request.headers)
print(str(response.status_code) + " " + response.reason)
print(response.text)
print()



# Ask for username and password from user
username = input("Username: ")
passwd = getpass() 



headers = {'content-type': 'applicatiob/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
response = sess.put(baseURL + "context/login/", json={"username": username, "password": passwd, "collection": 688130}, headers=headers)
cookies = response.cookies
csrftoken = response.cookies.get('csrftoken') # Keep and use new CSRF token after login
print(response.request)
#print(response.request.headers)

print(str(response.status_code) + " " + response.reason)
print(response.text)
print()



# Which user are logged in
headers = {'content-type': 'applicatiob/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
response = sess.get(baseURL + "context/user.json", headers=headers)
cookies = response.cookies
print(response.request)
#print(response.request.headers)
print(response.request.body)

print(str(response.status_code) + " " + response.reason)
print(response.text)
print()



# Query an object
headers = {'content-type': 'applicatiob/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
response = sess.get(baseURL + "api/specify/collectionobject/501269/", headers=headers)
cookies = response.cookies
print(response.request)
#print(response.request.headers)
print(response.request.body)

print(str(response.status_code) + " " + response.reason)
print(response.text)
print()



# Logout
headers = {'content-type': 'applicatiob/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
response = sess.put(baseURL + "context/login/", data="{\"username\": null, \"password\": null, \"collection\": 688130}", headers=headers)
cookies = response.cookies
print(response.request)
#print(response.request.headers)
print(response.request.body)

print(str(response.status_code) + " " + response.reason)
print(response.text)
print()

