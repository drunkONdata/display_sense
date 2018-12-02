# DisplaySense - Bringing Digital Analytics to the Storefront

## Table of Contents
1. [Motivation](#motivation)
2. [Product](#product)
3. [Gathering and Cleaning Data](#gathering-and-cleaning-data)
4. [Data Preparation](#data-preparation)
5. [Modeling](#modeling)
6. [Usage](#usage)
7. [Future Work](#future-work)
8. [References](#references)
9. [License](#license)

## Motivation

How do retailers determine how successful a storefront is? How do they acquire data to quantify this success?

## Product

DisplaySense utilizes an ensemble of off-the-shelf hardware, open vision, facial expression sentiment analysis & deep learning techniques to quantify the effectiveness of a store front.  

Our solution is:
* Easily scalable to multiple stores, displays, aisles & security cameras
* Sensitive to customer’s privacy
* Is easily understandable via a centralized dashboard
* Can ensemble with other data sources

## Data Pipeline

### Video Stream Acquisition

Leverage existing and new hardware at storefronts to record video to be analyzed

### Deep Learning & Open Vision

Extract demographic & sentiment features from video for analysis using AWS Rekognition

### DisplaySense Analytics

Display aggregated impressions & data of storefront in a dashboard

## Data Workflow

### Overview 

![](https://i.imgur.com/d7tk2dS.png)

### Components

#### 1. Video Stream

This can be a live stream from a camera or video recorded previously.

#### 2. AWS S3 Bucket

The video is pushed to an S3 bucket in order to easily interact with other AWS services in the next steps.

#### 3. AWS Rekognition

Video is analyzed for information on human faces that have been detected in the video.

#### 4. AWS SNS

Once Rekognition has completed a job SNS notifies and pushes the result to a queue. 

#### 5. AWS SQS

First-in, first-out queue that allows us to retrieve the results of completed jobs.

#### 6. Dashboard

Displays aggregate results from the analyzed video data. 

## Modeling



## Usage



## Future Work


## Tech Stack

<img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" width="250">
<img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/NumPy_logo.svg" width="250">
<img src="https://pandas.pydata.org/_static/pandas_logo.png" width="250">
<img src="https://cdn-images-1.medium.com/max/1600/1*AD9ZSLXKAhZ-_WomszsmPg.png" width="250">
<img src="https://camo.githubusercontent.com/630f51296667710aa4dd5959ec5cbc9c03bd48ac/687474703a2f2f7777772e6168612e696f2f6173736574732f6769746875622e37343333363932636162626661313332663334616462303334653739303966612e706e67" width="250">
<img src="http://flask.pocoo.org/static/logo/flask.png" width="250">
<img src="https://cdn-images-1.medium.com/max/1800/1*5mFQsJUF4FcVAaTJSPI0aA.png" width="250">

## References


## License
MIT License

Copyright (c) 2018 Abhi Banerjee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
