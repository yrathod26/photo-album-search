import json
import boto3
import urllib3
import time

def lambda_handler(event, context):
    # TODO implement
    print(event)
    url_ES = "https://vpc-es-hw3-vtndw6jsxco2bkxcv3ugwu4zcm.us-east-1.es.amazonaws.com/es-hw3/labels"
    # url_ES = "https://vpc-es-hw3-vtndw6jsxco2bkxcv3ugwu4zcm.us-east-1.es.amazonaws.com/es-hw3/_search?q=man"
    image_name = event['Records'][0]['s3']['object']['key']
    bucketName = "cc-hw3-photos"
    client = boto3.client('rekognition')
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucketName,
                'Name': image_name
            }
        },
        MinConfidence = 55.0
    )
    labelsList = []
    for label in response['Labels']:
        labelsList.append(label['Name'])
    http = urllib3.PoolManager()
    data = {}
    data['objectKey'] = image_name
    data['bucket'] = bucketName
    # data['createdTimestamp'] = time.time()
    data['labels'] = labelsList
    data = json.dumps(data)
    print(data)
    print(labelsList)
    headers = { "Content-Type": "application/json" }
    r = http.request('POST',url_ES,body=data,headers = headers)
    # r = http.request('GET',url_ES)
    print(r.data)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
