import csv
import os
import requests
import datetime

def getToken(clientId,clientSecret):
    tokenUrl = "https://id.twitch.tv/oauth2/token"
    grantType = "client_credentials",

    r = requests.post(tokenUrl,params={
        'client_id' : clientId,
        'client_secret' : clientSecret,
        'grant_type':grantType
    })

    result = r.json()
    print(result)
    return "Bearer " + result["access_token"]

def getStreamersFromTwitch(authorization,clientId,streamParams):
    jsonStreamerUrl = "https://api.twitch.tv/helix/streams"
    r = requests.get(jsonStreamerUrl,streamParams,headers={
        'Authorization' : authorization,
        'Client-id' :   clientId
    })

    return r.json()

def getJsonsStreamersListFromTwitch(authorization,clientId,amount,streamParams):
    resultList = []
    for i in range(amount):
        result = []
        result = getStreamersFromTwitch(authorization,clientId,streamParams)
        if(i > 0):
            cursor = result['pagination']['cursor']
            streamParams['after'] = cursor
        resultList.append(result)

    return resultList

def saveJsonsToCsv(jsonsList,timeOfData,csvFileName):
    for jsonContent in jsonsList:
        saveJsonToCsv(jsonContent,timeOfData,csvFileName)

def saveJsonToCsv(jsonContent,timeOfData,csvFileName):
    with open(csvFileName,'a',newline='',encoding="UTF-8") as csvFile:
        csvWriter = csv.writer(csvFile)
        if os.stat(csvFileName).st_size <= 0:
            head = ['id','user_id','user_login', 'user_name','game_id','game_name','type','title','viewer_count','started_at','language','is_mature','timeOfData']
            csvWriter.writerow(head)
        #write header
        for row in jsonContent['data']:
            rowWithData = [
                row['id'],
                row['user_id'],
                row['user_login'],
                row['user_name'],
                row['game_id'],
                row['game_name'],
                row['type'],
                row['title'],
                row['viewer_count'],
                row['started_at'],
                row['language'],
                row['is_mature'],
                timeOfData
                ]
            csvWriter.writerow(rowWithData)
            
def scrapTheData(csvFilePrefix,clientId,secret,gameIds,amount,token="empty"):
    requestParams = {
        'game_id' : gameIds,
        'first': 100
    }
    current_time = datetime.datetime.now() 
    csvFileName = csvFilePrefix + current_time.strftime("_%Y-%m-%d_") + current_time.strftime("%H_%M_%S") + ".csv"
    print(csvFileName)

    if(token == "empty"):
        authorizationHeader = getToken(clientId,secret)
    else:
        authorizationHeader = token
    
    jsonResultList = getJsonsStreamersListFromTwitch(authorizationHeader,clientId,amount,requestParams)
    saveJsonsToCsv(jsonResultList,current_time,csvFileName)


