import boto3
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    rekognition = boto3.client('rekognition')
    line_bot_api = LineBotApi('YOUR_LINE_CHANNEL_ACCESS_TOKEN')  # LINE_CHANNEL_ACCESS_TOKEN

    # 取得 S3 上的照片
    bucket = 'YOUR_S3_BUCKET name'
    key = 'saved.png' #你的圖片位置
    response = s3.get_object(Bucket=bucket, Key=key)
    image_bytes = response['Body'].read()

    rekog_response = rekognition.detect_faces(
        Image={'Bytes': image_bytes},
        Attributes=['ALL']
    )

    # 提取訊息
    faces = rekog_response['FaceDetails']

    for face in faces:
        emotions = face.get('Emotions', [])
        max_emotion = max(emotions, key=lambda x: x['Confidence'])
        person_name = 'Unknown'


        message = f"Hello {person_name}! Detected emotion: {max_emotion['Type']} with confidence {max_emotion['Confidence']:.2f}%"
        line_bot_api.push_message('USER_ID', TextSendMessage(text=message))
            
        image_message = ImageSendMessage(original_content_url=f'https://{bucket}.s3.amazonaws.com/{key}', preview_image_url=f'https://{bucket}.s3.amazonaws.com/{key}')
        line_bot_api.push_message('USER_ID', image_message)

    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }
