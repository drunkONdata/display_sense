# DisplaySense - Delivering storefront intelligence

## Table of Contents:
1. [Motivation](#motivation)
2. [Product](#product)
3. [Data Workflow & Pipeline](#Data-Workflow-&-Pipeline)
4. [Data Preparation](#data-preparation)
5. [Modeling](#modeling)
6. [Usage](#usage)
7. [Future Work](#future-work)
8. [References](#references)
9. [License](https://github.com/drunkONdata/storefront_analytics/blob/master/LICENSE)

## Motivation:
How do retailers determine how successful a storefront is? How do they acquire data to quantify this success? 

## Product:
DisplaySense utilizes an ensemble of off-the-shelf hardware, open vision, facial expression sentiment analysis & deep learning techniques to quantify the effectiveness of a store front. Our solution is:
* Easily scalable to multiple stores, displays, aisles & security cameras
* Sensitive to customer’s privacy
* Is easily understandable via a centralized dashboard
* Can ensemble with other data sources

## Data Workflow & Pipeline:

### Video Stream Acquisition
Leverage existing and new hardware at storefronts to record video to be analyzed

### Deep Learning & Open Vision
Extract demographic & sentiment features from video for analysis using AWS Rekognition

### DisplaySense Analytics
Display aggregated impressions & data of storefront in a dashboard

![](https://i.imgur.com/d7tk2dS.png)

#### 1. Video Stream
This can be a live stream from a camera or video recorded previously

#### 2. AWS S3 Bucket
The video is pushed to an S3 bucket in order to easily interact with other AWS services in the next steps

#### 3. AWS Rekognition
Video is analyzed for information on human faces that have been detected in the video

#### 4. AWS SNS
Once Rekognition has completed a job SNS notifies and pushes the result to a queue

#### 5. AWS SQS
First-in, first-out queue that allows us to retrieve the results of completed jobs

#### 6. Dashboard
Displays aggregate results from the analyzed video data

## Modeling



## Usage



## Future Work


## Tech Stack:
<p align="center">
<img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" width="250">
<img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/NumPy_logo.svg" width="250">
<img src="https://pandas.pydata.org/_static/pandas_logo.png" width="250">
<img src="https://cdn-images-1.medium.com/max/1600/1*AD9ZSLXKAhZ-_WomszsmPg.png" width="250">
<img src="https://camo.githubusercontent.com/630f51296667710aa4dd5959ec5cbc9c03bd48ac/687474703a2f2f7777772e6168612e696f2f6173736574732f6769746875622e37343333363932636162626661313332663334616462303334653739303966612e706e67" width="250">
<img src="http://flask.pocoo.org/static/logo/flask.png" width="250">
<img src="https://cdn-images-1.medium.com/max/1800/1*5mFQsJUF4FcVAaTJSPI0aA.png" width="250">
</p>


## References


