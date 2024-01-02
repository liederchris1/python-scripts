import requests, json
import pandas as pd
import openpyxl


auth0Token = ''
quantiveSysadminToken =''
auth0Headers = {
    'Authorization': f'Bearer {auth0Token}'
}
auth0_domain = 'auth.us.gtmhub.com'

quantiveHeaders = {
    'authorization': f"Bearer {quantiveSysadminToken}",
    'gtmhub-accountid': '',
    'ContentType': 'application/json'

}

def getClientID(email):
    url = 'https://auth.us.gtmhub.com/api/v2/users-by-email?email='
    email = email
    #print(url+email)
    headers = auth0Headers
    response = requests.get(url + email, headers=headers)
    r = response.json()
    print(r[0]['user_id'])
    return r[0]['user_id']


def getPrimarySecondary(clientID):
    url = 'https://app.us.gtmhub.com/api/v1/users/accounts/' + clientID
    headers = quantiveHeaders
    response = requests.get(url, headers=headers)
    #print(response)
    userinfo = dict()
    r = response.json()
    # print(r)
    for i in range(0, len(r)):
        if r[i]['accountId'] == '':
            userinfo.update({'newPrimaryUserID': r[i]['userId']})
            userinfo.update({'newPrimaryAccountID': r[i]['accountId']})
        if r[i]['accountId'] == '':
            userinfo.update({'newSecondaryAccountID': r[i]['accountId']})
            userinfo.update({'newSecondaryUserID': r[i]['userId']})
    #print(userinfo)
    return userinfo


def switchPrimarySecondary(userInfo):
    url = 'https://app.us.quantive.com/api/v1/users/multi/switch'
    headers = quantiveHeaders
    body = {
    "currentPrimaryUser": {

       "userId": userInfo["newSecondaryUserID"],
        "accountId": userInfo["newSecondaryAccountID"]
    },
    "newPrimaryUser": {
       "userId": userInfo["newPrimaryUserID"],
        "accountId": userInfo["newPrimaryAccountID"]
    }
    }
    print(body)
    response = requests.post(url, data=json.dumps(body),  headers=headers)
    print(f'Switch Primary response: {response}')

def getUserAuth0(clientID):
    url = f'https://auth.us.gtmhub.com/api/v2/users/{clientID}'
    headers = auth0Headers
    response = requests.get(url, headers=headers)
    jsonResponse = response.json()
    #print(jsonResponse)
    return jsonResponse

def unlinkAccountAuth0(jsonResponse):
    headers = auth0Headers
    userInformation = {
        'email': jsonResponse['email'],
        'secondaryUserId': jsonResponse['identities'][1]['user_id'],
        'secondaryProvider': jsonResponse['identities'][1]['provider'],
        'primaryUserId': jsonResponse['user_id']
    }
    primaryUserId = userInformation['primaryUserId']
    secondaryUserId = userInformation['secondaryUserId']
    secondaryProvider = userInformation['secondaryProvider']
    url = f'https://{auth0_domain}/api/v2/users/{primaryUserId}/identities/{secondaryProvider}/{secondaryUserId}'
    print(url)
    response = requests.delete(url, headers = headers)
    print(f'Account Unlinked - UserID: {secondaryUserId} - Response: {response}')
    return f'{secondaryProvider}|{secondaryUserId}'


def deleteNewAuth0Profile(secondaryClientId):
    headers = auth0Headers
    url = f'https://{auth0_domain}/api/v2/users/{secondaryClientId}'
    print(url)
    response = requests.delete(url, headers = headers)
    print(f'Account Deleted - UserID: {secondaryClientId} - Response: {response}')
    return


def updateDBAuth0Cache(email):
    clientId2 = getClientID(email)
    headers = auth0Headers
    body = getUserAuth0(clientId2)
    url = f'https://app.us.gtmhub.com/api/v1/users/cache/{clientId2}'
    response = requests.put(url, data=json.dumps(body))
    print(f'Updated DB cache for user: {clientId2} - Response: {response}')
    return



def fn():
    emails = pd.read_excel("fileName", "SheetName")
    for x in range(0,len(emails.index)):
        # functions to remove old sso connection in order to switch primary and secondary
        # clientId = getClientID(emails.iloc[x,1])
        # userAuth0Json = getUserAuth0(clientId)
        # secondaryClientId = unlinkAccountAuth0(userAuth0Json)
        # deleteNewAuth0Profile(secondaryClientId)
        # updateDBAuth0Cache(emails.iloc[x,1])

        # functions to switch primary and secondary
        print(emails.iloc[x,1])
        clientId = getClientID(emails.iloc[x,1])
        getUserAuth0(clientId)
        userinfo = getPrimarySecondary(clientId)
        switchPrimarySecondary(userinfo)

#clientId = getClientID('')
# userInfo = getUserAuth0(clientId)
# unlinkAccountAuth0(userInfo)

fn()
