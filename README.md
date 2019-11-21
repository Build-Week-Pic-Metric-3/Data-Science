# Pic Metric 3 - Data Science API
Build on Deep Learning AMI (Amazon Linux) Version 25.3 - ami-028a41f747ffea9c0 using a g4dn.xlarge ec2 instance.

## Setup

Upon loading the server run the bootstrap.sh file, then create the .ev file.
Reference .env file, place in the Repo folder:

```
FLASK_ENV='development'
FLASK_APP='PicMetric:APP'

DATABASE_URL='postgres://Username:Password@URL:5432/table'

S3_KEY = 'KEYGOESHERE'
S3_SECRET = 'SECRETGOESHERE'
S3_BUCKET = 'BUCKETGOESHERE'
S3_LOCATION = 'http://BUCKETNAME.s3.amazonaws.com/'

ExtraArgs='{"ACL": "public-read", "ContentType": "image/png", "ContentDisposition": "inline"}'
```

To run the app, go into the Repo folder and run
`gunicorn -t 120 "PicMetric:create_app()"`


## Models
* Res Net 50 - Trained on 1,000 classes in object recognition!
* Yolo_V3 Coco - "You Only Look Once" - Trained on 80 classes in object recognition, and idenifies bounding boxes for objects are in the images 
* MTCNN - Multi-task Cascaded Convolutional Neural Networks for Face Detection. Trained on faces, and draws where the Neural Network identifies faces and where eyes/mouth/nose are located.

## Use


With the Flask App running, you are able to use the `:5000/upload` path to verify both uploaded images and posted URLS will work.


Lets use a test image:


### Original Image
![Original](http://picmetric3.s3.amazonaws.com/4f055f233ff79efdb5fdd377b2161c45.png)



It will take ~30 seconds to churn through all the Neural Networks, when completed a response JSON is returned:

`{
  "error": "",
  "faces_source": "http://picmetric3.s3.amazonaws.com/c19b284ae9180e15d537ffe66ddebf8d_faces.png",
  "hash": "4f055f233ff79efdb5fdd377b2161c45",
  "original": "http://picmetric3.s3.amazonaws.com/4f055f233ff79efdb5fdd377b2161c45.png",
  "resnet": "{\"studio_couch\": \"0.7868622\", \"library\": \"0.055205315\", \"window_shade\": \"0.024714082\"}",
  "yolov3": "{\"potted plant\": \"67.16461777687073\", \"couch\": \"95.92761397361755\", \"person\": \"99.80075359344482\"}",
  "yolov3_source": "http://picmetric3.s3.amazonaws.com/c19b284ae9180e15d537ffe66ddebf8d_yolov3.png"
}`

* error catches = (some) errors on the server
* faces_source = S3 Path drawing the facial identification shared from the MCTNN
* hash = md5 hash of the original uploaded image - used to prevent duplicate photos from being processed
* original = original image sent via upload or link, but hosted in s3!
* resnet = The objects detected, and the percent certainty it was detected in the photo.
* yolov3 = What objects were detected in the image according to yolov3, and percent certainty of the prediction.
* yolov3_source = The bounding boxes identified by yolov3


###  Yolo_v3 analyzed Image: 
![Yolo](http://picmetric3.s3.amazonaws.com/c19b284ae9180e15d537ffe66ddebf8d_yolov3.png)


### MTCNN analyzed Image:
![MTCNN](http://picmetric3.s3.amazonaws.com/c19b284ae9180e15d537ffe66ddebf8d_faces.png)

## To Do

* Optimize time to return images, parrelizing jobs either within the flask app or by distributing across AWS Sagemaker.


