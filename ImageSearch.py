import json
import urllib3
import boto3
import urllib

lex = boto3.client('lex-runtime')

def lambda_handler(event, context):
    # TODO implement
    print(event)
    text = str(event['queryStringParameters']['text']).replace('+',' ')
    response = lex.post_text(
        botName = "ImgSearchBot",
        botAlias = "$LATEST",
        userId = "admin",
        inputText = text
    )
    slots = response['slots']
    slot1 = slots['searchObjA']
    slot2 = slots['searchObjB']
    slot3 = slots['searchObjC']
    list1 = searchByTag(slot1)
    if (slot2 != None and slot2.strip() != ""):
        list2 = searchByTag(slot2)
        list1 = list(set(list1).union(set(list2)))
    if (slot3 != None and slot3.strip() != ""):
        list3 = searchByTag(slot3)
        list1 = list(set(list1).union(set(list3)))
    print(list1)
    return {
        'statusCode': 200,
        'headers': {
          'Access-Control-Allow-Origin': '*'
         },
        'body':json.dumps(list1)
    }

def searchByTag(keyword):
    
    url_ES = "https://vpc-es-hw3-vtndw6jsxco2bkxcv3ugwu4zcm.us-east-1.es.amazonaws.com/es-hw3/_search?q=" + keyword
    http = urllib3.PoolManager()
    r = http.request('GET',url_ES)
    data = r.data.decode('utf-8')
    data = json.loads(data)
    list=[]
    for photos in data['hits']['hits']:
        bucket = photos["_source"]["bucket"]
        key = photos["_source"]["objectKey"]
        list.append("https://s3.amazonaws.com/"+bucket+"/"+key)
        
    return list