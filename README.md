<p align="center">
<img src="images/displaysense_logo.png">
# DisplaySense - Delivering storefront intelligence

## Table of Contents:
1. [Motivation](#motivation)
2. [Product](#product)
3. [Data Workflow and Pipeline](#data-workflow-and-pipeline)
4. [Deployment](#deployment)
5. [Future Work](#future-work)
6. [References](#references)
7. [License](https://github.com/drunkONdata/storefront_analytics/blob/master/LICENSE)

## Motivation:
How do retailers determine how successful a storefront is? How do they acquire data to quantify this success? 

## Product:
DisplaySense utilizes an ensemble of off-the-shelf hardware, open vision, facial expression sentiment analysis & deep learning techniques to quantify the effectiveness of a store front. Our solution is:
* Easily scalable to multiple stores, displays, aisles & security cameras
* Sensitive to customer’s privacy
* Is easily understandable via a centralized dashboard
* Can ensemble with other data sources

## Data Workflow and Pipeline

### Video Stream Acquisition
Leverage existing and new hardware at storefronts to record video to be analyzed

### Deep Learning & Open Vision
Extract demographic & sentiment features from video for analysis using AWS Rekognition

### DisplaySense Analytics
Display aggregated impressions & data of storefront in a dashboard

![](https://i.imgur.com/d7tk2dS.png)

#### 1. Video Stream
This can be a live stream from a camera or video recorded previously.

#### 2. AWS S3 Bucket
The video is pushed to an S3 bucket in order to easily interact with other AWS services in the next steps.

#### 3. AWS Rekognition
The stored video is then analyzed to detect persons, faces, gender, age, sentiments, facial features such as beard, mustache, eyeglasses etc.

#### 4. AWS Simple Notification Service (SNS)
Amazon Rekognition Video publishes the completion status of the video analysis to an Amazon SNS topic. If the video analysis is successful, you can get the results of the video analysis.

#### 5. AWS Simple Queue Service (SQS)
First-in, first-out Amazon SQS queue to get the completion status of the video analysis request. The response sent back by the SQS queue is a json object.

#### 6. Dashboard
Displays aggregate results to show person and face traffic, gender and age composition, general mood from the analyzed video data(json object sent back by SQS queue).

## Deployment

Anaconda is the recommended solution for installing and managing the packages necessary for DisplaySense analytics. Please see the Anaconda [installation instructions](http://docs.anaconda.com/anaconda/install/).  

The `requirements.txt` file lists all Python libraries necessary for utilizing DisplaySense, and they will be installed using the following commands:

`pip install -r requirements.txt`
`conda install -r requirements.txt`

AWS Identity and Access Management (IAM) must be configured to manage access to AWS services and resources securely. Please see Amazon's [getting set up](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-set-up.html) documentation. 

Once AWS access has been established the AWS SNS and AWS SQS steps of the data pipeline can be configured as well.

Please see the [SNS documentation](https://aws.amazon.com/sns/getting-started/) for configuring an SNS Topic and the [SQS documentation](https://aws.amazon.com/sqs/getting-started/) for configuring a queue. 

## Future Work


## Tech Stack:
<p align="center">
<img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" width="250">
<img src="images/spacer.png">
<img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/NumPy_logo.svg" width="250">
<img src="images/spacer.png">
<img src="https://pandas.pydata.org/_static/pandas_logo.png" width="250">
<img src="images/spacer.png">
<img src="https://cdn-images-1.medium.com/max/1600/1*AD9ZSLXKAhZ-_WomszsmPg.png" width="250">
<img src="images/spacer.png">
<img src="https://upload.wikimedia.org/wikipedia/commons/3/32/OpenCV_Logo_with_text_svg_version.svg" width="125">
<img src="images/spacer.png">
<img src="http://flask.pocoo.org/static/logo/flask.png" width="250">
<img src="images/spacer.png">
<img src="https://blog.f1000.com/wp-content/uploads/2017/07/logo.png" width="250"> 
</p>


## References
https://docs.aws.amazon.com/rekognition/#lang/en_us
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html
https://people.eecs.berkeley.edu/~jordan/sail/readings/rubin.pdf
http://flask.pocoo.org/docs/1.0/
https://plot.ly/python/#fundamentals



