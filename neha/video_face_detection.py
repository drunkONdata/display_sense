#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#SPDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-s3-developer-guide/blob/master/LICENSE-SAMPLECODE.)

#Example code for calling Rekognition Video operations
#For more information, see https://docs.aws.amazon.com/rekognition/latest/dg/video.html

import boto3
import json
import sys

#Analyzes videos using the Rekognition Video API 
class VideoDetect:
    jobId = ''
    rek = boto3.client('rekognition')
    # queueUrl = 'https://sqs.us-west-2.amazonaws.com/302497794745/Reko_SNS_Queue.fifo'
    queueUrl = 'https://sqs.us-west-2.amazonaws.com/302497794745/Reko_std_queue'
    roleArn = 'arn:aws:iam::302497794745:role/Rekognition_SNS'
    topicArn = 'arn:aws:sns:us-west-2:302497794745:Rekognition_topic'
    bucket = 'storefront-analytics'
    video = 'bezos_vogels.mp4'

    #Entry point. Starts analysis of video in specified bucket.
    def main(self, task):
        """
        This function writes a list of time_stamp,images into a video named using
        the name parameter and the first time stamp in the image list.

        Args:
            task: Name of the task as a string. Valid choices are label_detection, face_detection,
            face_search, person_tracking, celebrity_recognition, content_moderation

        Returns:
            results: list of json responses returned by AWS SQS queue
        """

        jobFound = False
        sqs = boto3.client('sqs')
       
        # Changes according to the task chosen by the user.
        #=====================================
        if task == 'label_detection':
            response = self.rek.start_label_detection(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
                                            NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.topicArn})
        elif task == 'face_detection':
            response = self.rek.start_face_detection(Video={'S3Object':{'Bucket':self.bucket,'Name':self.video}},
            NotificationChannel={'RoleArn':self.roleArn, 'SNSTopicArn':self.topicArn}, FaceAttributes='ALL') 

        elif task == 'face_search':
            response = self.rek.start_face_search(Video={'S3Object':{'Bucket':self.bucket,'Name':self.video}},
            CollectionId='CollectionId',
            NotificationChannel={'RoleArn':self.roleArn, 'SNSTopicArn':self.topicArn})

        elif task == 'person_tracking':
            response = self.rek.start_person_tracking(Video={'S3Object':{'Bucket':self.bucket,'Name':self.video}},
            NotificationChannel={'RoleArn':self.roleArn, 'SNSTopicArn':self.topicArn})

        elif task == 'celebrity_recognition':
            response = self.rek.start_celebrity_recognition(Video={'S3Object':{'Bucket':self.bucket,'Name':self.video}},
            NotificationChannel={'RoleArn':self.roleArn, 'SNSTopicArn':self.topicArn})

        elif task == 'content_moderation':
            response = self.rek.start_content_moderation(Video={'S3Object':{'Bucket':self.bucket,'Name':self.video}},
            NotificationChannel={'RoleArn':self.roleArn, 'SNSTopicArn':self.topicArn})        


        #=====================================
        print('Start Job Id: ' + response['JobId'])
        dotLine=0
        while jobFound == False:
            sqsResponse = sqs.receive_message(QueueUrl=self.queueUrl, MessageAttributeNames=['ALL'],
                                          MaxNumberOfMessages=10)

            if sqsResponse:
                
                if 'Messages' not in sqsResponse:
                    if dotLine<20:
                        print('.', end='')
                        dotLine=dotLine+1
                    else:
                        print()
                        dotLine=0    
                    sys.stdout.flush()
                    continue

                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    rekMessage = json.loads(notification['Message'])
                    print(rekMessage['JobId'])
                    print(rekMessage['Status'])
                    if str(rekMessage['JobId']) == response['JobId']:
                        print('Matching Job Found:' + rekMessage['JobId'])
                        jobFound = True
                        #Changes according to the task chosen by user.
                        #=============================================
                        if task == 'label_detection':
                            results = self.GetResultsLabels(rekMessage['JobId'])
                        elif task == 'face_detection':
                            results = self.GetResultsFaces(rekMessage['JobId']) 
                        elif task == 'face_search':
                            results = self.GetResultsFaceSearchCollection(rekMessage['JobId'])
                        elif task == 'person_tracking':
                            results = self.GetResultsPersons(rekMessage['JobId']) 
                        elif task == 'celebrity_recognition':
                            results = self.GetResultsCelebrities(rekMessage['JobId']) 
                        elif task == 'content_moderation':
                            results = self.GetResultsModerationLabels(rekMessage['JobId'])                    
                                                
                        #=============================================

                        sqs.delete_message(QueueUrl=self.queueUrl,
                                       ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" +
                              str(rekMessage['JobId']) + ' : ' + str(response['JobId']))
                    # Delete the unknown message. Consider sending to dead letter queue
                    sqs.delete_message(QueueUrl=self.queueUrl,
                                   ReceiptHandle=message['ReceiptHandle'])

        print('done')
        return results


    # Gets the results of labels detection by calling GetLabelDetection. Label
    # detection is started by a call to StartLabelDetection.
    # jobId is the identifier returned from StartLabelDetection
    def GetResultsLabels(self, jobId):
        maxResults = 500
        paginationToken = ''
        finished = False
        results = []

        while finished == False:
            response = self.rek.get_label_detection(JobId=jobId,
                                            MaxResults=maxResults,
                                            NextToken=paginationToken,
                                            SortBy='TIMESTAMP')

            print(response['VideoMetadata']['Codec'])
            print(str(response['VideoMetadata']['DurationMillis']))
            print(response['VideoMetadata']['Format'])
            print(response['VideoMetadata']['FrameRate'])

            for labelDetection in response['Labels']:
                print(labelDetection['Label']['Name'])
                print(labelDetection['Label']['Confidence'])
                print(str(labelDetection['Timestamp']))
                results.append(labelDetection)

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

        return results

    # Gets person tracking information using the GetPersonTracking operation.
    # You start person tracking by calling StartPersonTracking
    # jobId is the identifier returned from StartPersonTracking
    def GetResultsPersons(self, jobId):
        maxResults = 10
        paginationToken = ''
        finished = False
        results = []

        while finished == False:
            response = self.rek.get_person_tracking(JobId=jobId,
                                            MaxResults=maxResults,
                                            NextToken=paginationToken)

            print(response['VideoMetadata']['Codec'])
            print(str(response['VideoMetadata']['DurationMillis']))
            print(response['VideoMetadata']['Format'])
            print(response['VideoMetadata']['FrameRate'])

            for personDetection in response['Persons']:
                print('Index: ' + str(personDetection['Person']['Index']))
                print('Timestamp: ' + str(personDetection['Timestamp']))
                print(personDetection)
                results.append(personDetection)

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

        return results

    # Gets the results of unsafe content label detection by calling
    # GetContentModeration. Analysis is started by a call to StartContentModeration.
    # jobId is the identifier returned from StartContentModeration
    def GetResultsModerationLabels(self, jobId):
        maxResults = 500
        paginationToken = ''
        finished = False
        results = []

        while finished == False:
            response = self.rek.get_content_moderation(JobId=jobId,
                                                MaxResults=maxResults,
                                                NextToken=paginationToken)

            print(response['VideoMetadata']['Codec'])
            print(str(response['VideoMetadata']['DurationMillis']))
            print(response['VideoMetadata']['Format'])
            print(response['VideoMetadata']['FrameRate'])

            for contentModerationDetection in response['ModerationLabels']:
                print('Label: ' +
                    str(contentModerationDetection['ModerationLabel']['Name']))
                print('Confidence: ' +
                    str(contentModerationDetection['ModerationLabel']['Confidence']))
                print('Parent category: ' +
                    str(contentModerationDetection['ModerationLabel']['ParentName']))
                print('Timestamp: ' + str(contentModerationDetection['Timestamp']))
                print()
                results.append(contentModerationDetection)

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

        return results

    # Gets the results of face detection by calling GetFaceDetection. Face 
    # detection is started by calling StartFaceDetection.
    # jobId is the identifier returned from StartFaceDetection
    def GetResultsFaces(self, jobId):
        maxResults = 500
        paginationToken = ''
        finished = False
        results = []

        while finished == False:
            response = self.rek.get_face_detection(
                JobId=jobId,
                MaxResults=maxResults,
                NextToken=paginationToken)

            print(response['VideoMetadata']['Codec'])
            print(str(response['VideoMetadata']['DurationMillis']))
            print(response['VideoMetadata']['Format'])
            print(response['VideoMetadata']['FrameRate'])

            for faceDetection in response['Faces']:
                print('Face: ' + str(faceDetection['Face']))
                print('Confidence: ' + str(faceDetection['Face']['Confidence']))
                print('Timestamp: ' + str(faceDetection['Timestamp']))
                print()
                results.append(faceDetection)

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

        return results

    # Gets the results of a collection face search by calling GetFaceSearch.
    # The search is started by calling StartFaceSearch.
    # jobId is the identifier returned from StartFaceSearch
    def GetResultsFaceSearchCollection(self, jobId):
        maxResults = 500
        paginationToken = ''
        finished = False
        results = []

        while finished == False:
            response = self.rek.get_face_search(
                JobId=jobId,
                MaxResults=maxResults,
                NextToken=paginationToken)

            print(response['VideoMetadata']['Codec'])
            print(str(response['VideoMetadata']['DurationMillis']))
            print(response['VideoMetadata']['Format'])
            print(response['VideoMetadata']['FrameRate'])

            for personMatch in response['Persons']:
                print('Person Index: ' + str(personMatch['Person']['Index']))
                print('Timestamp: ' + str(personMatch['Timestamp']))

                if ('FaceMatches' in personMatch):
                    for faceMatch in personMatch['FaceMatches']:
                        print('Face ID: ' + faceMatch['Face']['FaceId'])
                        print('Similarity: ' + str(faceMatch['Similarity']))
                print()
                results.append(personMatch)

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True
            print()
        
        return results

    # Gets the results of a celebrity detection analysis by calling GetCelebrityRecognition.
    # Celebrity detection is started by calling StartCelebrityRecognition.
    # jobId is the identifier returned from StartCelebrityRecognition    
    def GetResultsCelebrities(self, jobId):
        maxResults = 500
        paginationToken = ''
        finished = False
        results = []

        while finished == False:
            response = self.rek.get_celebrity_recognition(JobId=jobId,
                                                    MaxResults=maxResults,
                                                    NextToken=paginationToken)

            print(response['VideoMetadata']['Codec'])
            print(str(response['VideoMetadata']['DurationMillis']))
            print(response['VideoMetadata']['Format'])
            print(response['VideoMetadata']['FrameRate'])

            for celebrityRecognition in response['Celebrities']:
                print('Celebrity: ' +
                    str(celebrityRecognition['Celebrity']['Name']))
                print('Timestamp: ' + str(celebrityRecognition['Timestamp']))
                print()
                results.append(celebrityRecognition)

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

        return results


if __name__ == "__main__":
    analyzer=VideoDetect()
    person_analysis = analyzer.main(task='person_tracking')
    print(person_analysis)