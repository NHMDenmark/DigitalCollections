# -*- coding: utf-8 -*-
"""
Script illustrating how to use the Specify API from a script
Needs requests installed, e.g.
pip install requests

Created on Thu June 16 2022

@author: Kim Steenstrup Pedersen, NHMD

Copyright 2022 Natural History Museum of Denmark (NHMD)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and 
limitations under the License. 
"""

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

