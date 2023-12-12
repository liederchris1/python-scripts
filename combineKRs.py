import json
import xlwt
from xlwt import Workbook
import requests

getMetricId = ''
postMetricId = ''
getIdArray = ['', '', '']
postUrl = f'https://app.us.quantive.com/api/v1/metrics/{postMetricId}/checkin'
getUrl = f'https://app.us.quantive.com/api/v1/metrics/{getMetricId}'
accountId = ''
token = 'Bearer...'
headers = {
    'Authorization': token,
    'gtmhub-accountId': accountId,
    'Content-type': 'application/json'

}


def getSnapshots():
    metric = requests.get(url=getUrl, headers=headers)
    print(metric.json())
    metrics = metric.json()
    #session = metrics.json()['sessionId']
    #print(session)
    updates = metrics['metricHistory']
    print(updates)
    return updates

def fileOfUpdates(arr):
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    # naming the columns in the excel sheet
    sheet1.write(0, 0, "Session ID")
    sheet1.write(0, 1, "KR Name")
    sheet1.write(0, 2, "Update Value")
    sheet1.write(0, 3, "Date and Time of Update")
    count = 1
    for i in range(0, len(arr)):
        url = f'https://app.us.quantive.com/api/v1/metrics/{arr[i]}'
        print(url)
        metric = requests.get(url=url, headers=headers)
        metricJson = metric.json()
        for i in range(0, len(metricJson['metricHistory'])):
            sheet1.write(count, 0, metricJson['sessionId'])
            sheet1.write(count, 1, metricJson['name'])
            sheet1.write(count, 2, metricJson['metricHistory'][i]['metricValue'])
            print(metricJson['metricHistory'][i]['metricValue'])
            sheet1.write(count, 3, metricJson['metricHistory'][i]['updatedAt'])
            count += 1
        wb.save('FileName')


def combineKRs(updates):
    for i in range(0, len(updates)):
        snapshot = {
            'actual': updates[i]['metricValue'],
            'checkInDate': updates[i]['updatedAt'],
            'confidence': updates[i]['confidenceValue'],
        }
        print(snapshot)
        response = requests.post(postUrl, data=json.dumps(snapshot), headers=headers)
        print(response)


def fileOfUpdates2(metrics):
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    # naming the columns in the excel sheet
    sheet1.write(0, 0, "KR Name")
    sheet1.write(0, 1, "Update Value")
    sheet1.write(0, 2, "Date and Time of Update")
    for i in range(0, len(metrics['metricHistory'])):
        sheet1.write(i+1, 0, metrics['name'])
        sheet1.write(i+1, 1, metrics['metricHistory'][i]['metricValue'])
        sheet1.write(i+1, 2, metrics['metricHistory'][i]['metricValue'])
    wb.save('fileName')

# snapshots = getSnapshots()
# combineKRs(snapshots)

fileOfUpdates(getIdArray)
