import requests


token = ''
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'gtmhub-accountid': ''
}

clientId = ''
accountIds = ['', '', '', '', '', '', '']
accountDomain = 'app.us.gtmhub.com'

def removeAccounts(ids):
    userId = ''
    accountid = ''
    url = f'https://{accountDomain}/api/v1/users/accounts/{clientId}'
    deleteURL = ''
    response = requests.get(url, headers=headers)
    accounts = response.json()
    for i in range(0, len(accounts)):
        if accounts[i]['accountId'] in ids:
            # print(accounts[i]['accountName'], accounts[i]['accountId'])
            userId = accounts[i]['userId']
            accountid = accounts[i]['accountId']
            deleteURL = f"https://{accountDomain}/api/v1/accounts/{accountid}/user/{userId}"
            # print(deleteURL)
            response2 = requests.delete(deleteURL, headers=headers)
            print(f"Account Name: {accounts[i]['accountName']} ... UserId: {accounts[i]['userId']} ... Account Id: {accounts[i]['accountId']} ... Response Code: {response2}")




removeAccounts(accountIds)