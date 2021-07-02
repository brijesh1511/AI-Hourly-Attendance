
#importing required libraries
import boto3
import requests
import datetime
import time
import cv2



#configuring credentials-----
client = boto3.client('rekognition',
                       aws_access_key_id = "provide your aws access key",
                       aws_secret_access_key = "provide your secret key ",
                       #aws_session_token = "provide your session token",
                       region_name = 'ap-south-1')




#capture images for every 1 hour and store the images with current date and time -----
for j in range (0,6):
    current_time = datetime.datetime.now().strftime("%d-%m-%y  %H-%M-%S")
    print(current_time)
    camera = cv2.VideoCapture(0)
    for i in range (20):
        return_value , image = camera.read()
        if (i == 19):
            cv2.imwrite('Hourly Class Images/' + current_time + '.jpg',image)
    del (camera)
#Sending the captured image to aws s3 bucket-----
    clients3 = boto3.client('s3',region_name = 'ap-south-1')
    clients3.upload_file('Hourly Class Images/' +current_timr+ '.jpg', 's3 bucket name',current_time + '.jpg')
#Recognise students in captured image-----
    with open(r'Hourly Class Images/'+current_time+'.jpg','rb') as source_image:
        source_bytes = source_image.read()
    print(type(source_bytes))
    print("Recognition Service")
    response = client.detect_custom_labels(
                        ProjectVersionArn = 'provide arn of your rekognition model',
                        Image = {
                            'Bytes' : source_bytes
                        },
    )
    print(response)
    if not len(response['CustomLabels']):
        print('Not identified')
        
    else:
        str1 = response['CustomLabels'][0]['Name']
        print(str1)
#Update the attendance of recognized student in dynamoDB by calling API-----
        url = "provide your add attendance api url link/test?Rollno=" +str1
        resp = requests.get(url)
        print(resp)
        if resp.status_code == 200:
            print("Success")
#to stop for 1 hour of a period.
    time.sleep(3600)







