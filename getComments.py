import requests
import xlwt
from xlwt import Workbook

# this script can be used to generate an excel file of comments left by a user in the account
# it is currently set up to only pull comments on key results, however this can easily be modified

userid = ''
accountid = ''
apiToken = ''
headers = {
    'Authorization': 'Bearer ' + apiToken,
    'Content-Type': 'application/json',
    'gtmhub-accountId': accountid
}

comment_url = "https://app.us.gtmhub.com/api/v1/comments"


def getUpdateComments():
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    # naming the columns in the excel sheet
    sheet1.write(0, 0, "KR Name")
    sheet1.write(0, 1, "Update Comment")
    sheet1.write(0, 2, "Date and Time")
    snapshot_url = "https://app.us.gtmhub.com/api/v2/metrics?skip="
    #print(arr[1])
    #print(arr[1]['metricHistory'])
    count = 0
    num = 100
    iterations = 0
    while num == 100:
        skip = str(iterations*100)
        print(snapshot_url+skip)
        responsecode = requests.get(snapshot_url+skip, headers=headers)
        print(responsecode)
        response = responsecode.json()
        arr = response['items']
        num = len(arr)
        print(num)
        for i in range(0, len(arr)):
            historyArr = arr[i]['metricHistory']
            for j in range(0, len(historyArr)):
                if (historyArr[j]['changedBy'] == userid) and (historyArr[j]['comment'] != ''):
                    sheet1.write(count + 1, 0, arr[i]['name'])
                    sheet1.write(count + 1, 1, historyArr[j]['comment'])
                    sheet1.write(count + 1, 2, historyArr[j]['createdAt'])
                    count += 1
        iterations += 1

    wb.save('fileName')





def getComments():
    # creating a new workbook to save output to
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    # naming the columns in the excel sheet
    sheet1.write(0,0,"KR Name")
    sheet1.write(0,1,"Comment")
    sheet1.write(0, 2, "Date and Time")
    # getting all comments in the account
    response = requests.get(comment_url, headers=headers).json()
    # saving response as an array
    arr = response['items']
    count = 0
    # iterating through array, if comment is left by a determined user
    # and is left on a KR write the comment and the KR name to the sheet
    for i in range(0,len(arr)):
        if (arr[i]['createdBy'] == userid) and (arr[i]['targetType'] == 'metric'):
            # print(arr[i])
            sheet1.write(count+1,0, arr[i]['targetTitle'])
            sheet1.write(count + 1, 1, arr[i]['text'])
            sheet1.write(count + 1, 2, arr[i]['createdAt'])
            count += 1
    # save the sheet
    wb.save('fileName')


getUpdateComments()
#test()
