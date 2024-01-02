# script that utilizes the sys admin moments endpoint to view specific moments for any account
import requests
import json
accountId = ''
accountDomain = 'https://app.gtmhub.com'
token = ''
targets = 'account'
url = accountDomain + '/api/v2/moments/' + accountId + '/?q=targets:' + targets + '&skip='
headers = {
    'authorization': "Bearer " + token,
    'gtmhub-accountid': '573dbb12ed915d0005cc2c46',
    'ContentType': 'application/json'

               }


def queryMoments():
    print("running")
    length = 10
    iterations = 0
    while(length == 10):
        skip = str(iterations * 10)
        print(url+skip)
        response = requests.get(url + skip, headers=headers).json()
        # print(response)
        arr = response['items']
        length = len(arr)
        for i in range(0, len(arr)):
            content = arr[i]['content']
            print(arr[i])
        iterations = iterations + 1


queryMoments()







