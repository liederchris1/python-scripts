import requests, json
import pandas as pd
import openpyxl
import numpy as np

headers = {
    'Authorization': 'Bearer ',
    'Content-Type': 'application/json',
    'gtmhub-accountid': ''
}

# for the read_excel function, the first argument is the name of the file,
# the file should be placed in the switchEmails Folder
# the 2nd argument is the name of the sheet containing the emails
# to work with the data in the excel file:
# consider it a 2D array, emails.iloc[row, column]
# Make sure to change the URL to include the right DC

emails = pd.read_excel("COSM Email Switch.xlsx", "Users")


def test():
    for x in range(len(emails.index)-1):
        url = f"https://app.us.gtmhub.com/api/v1/users/email/{emails.iloc[x, 1]}/"
        print("PATCH: " + url)
        print(f"NEW EMAIL: {emails.iloc[x,2]}")
        print(x)


def patchCall():
    for x in range(len(emails.index)-1):
        url = f"https://app.us.gtmhub.com/api/v1/users/email/{emails.iloc[x, 1]}/"
        #print(url)
        body = {
            "email": emails.iloc[x,2]
        }
        #print("New Email : " + emails.iloc[x,2])
        response = requests.patch(url, data=json.dumps(body), headers=headers)
        print(f'Updated User email: {emails.iloc[x,1]} to {emails.iloc[x,2]}... Response code: {response}')


def singleChange(old, new):
    url = "https://app.us.gtmhub.com/api/v1/users/email/"+ old +"/"
    body = {
        "email": new
    }
    print(body)
    response = requests.patch(url, data=json.dumps(body), headers=headers)
    print(response)


#test()


#patchCall()


#singleChange("","")
