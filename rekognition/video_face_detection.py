import boto3
import json
import sys

# Analyzes videos using the Rekognition Video API


class VideoDetect:

    def __init__(self, queue, roleArn, topicArn, bucket, video):
        self.queue = queue
        self.roleArn = roleArn
        self.topicArn = topicArn
        self.bucket = bucket
        self.video = video
        self.jobId = ''
        self.rek = boto3.client('rekognition')

    # Entry point. Starts analysis of video in specified bucket.
    def main(self, task):
        """
        This function writes a list of time_stamp, images into a video named
        using the name parameter and the first time stamp in the image list.

        Args:
            task: Name of the task as a string. Valid choices are
            label_detection, face_detection, face_search, person_tracking,
            celebrity_recognition, content_moderation

        Returns:
            results: list of json responses returned by AWS SQS queue
        """

        jobFound = False
        sqs = boto3.client('sqs')
        video = {'S3Object': {'Bucket': self.bucket, 'Name': self.video}}
        notification = {'RoleArn': self.roleArn, 'SNSTopicArn': self.topicArn}

        # Changes according to the task chosen by the user.
        # =====================================
        if task == 'label_detection':
            response = self.rek.start_label_detection(
                Video=video,
                NotificationChannel=notification)

        elif task == 'face_detection':
            response = self.rek.start_face_detection(
                Video=video,
                NotificationChannel=notification,
                FaceAttributes='ALL')

        elif task == 'face_search':
            response = self.rek.start_face_search(
                Video=video,
                NotificationChannel=notification,
                CollectionId='CollectionId')

        elif task == 'person_tracking':
            response = self.rek.start_person_tracking(
                Video=video,
                NotificationChannel=notification)

        elif task == 'celebrity_recognition':
            response = self.rek.start_celebrity_recognition(
                Video=video,
                NotificationChannel=notification)

        elif task == 'content_moderation':
            response = self.rek.start_content_moderation(
                Video=video,
                NotificationChannel=notification)
        # =====================================

        print('Start Job Id: ' + response['JobId'])
        dotLine = 0
        while jobFound is False:
            sqsResponse = sqs.receive_message(
                QueueUrl=self.queue,
                MessageAttributeNames=['ALL'],
                MaxNumberOfMessages=10)

            if sqsResponse:

                if 'Messages' not in sqsResponse:
                    if dotLine < 20:
                        print('.', end='')
                        dotLine = dotLine + 1
                    else:
                        print()
                        dotLine = 0
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

                        # Changes according to the task chosen by user.
                        # =============================================
                        if task == 'label_detection':
                            results = self.GetResultsLabels(
                                rekMessage['JobId'])
                        elif task == 'face_detection':
                            results = self.GetResultsFaces(
                                rekMessage['JobId'])
                        elif task == 'face_search':
                            results = self.GetResultsFaceSearchCollection(
                                rekMessage['JobId'])
                        elif task == 'person_tracking':
                            results = self.GetResultsPersons(
                                rekMessage['JobId'])
                        elif task == 'celebrity_recognition':
                            results = self.GetResultsCelebrities(
                                rekMessage['JobId'])
                        elif task == 'content_moderation':
                            results = self.GetResultsModerationLabels(
                                rekMessage['JobId'])
                        # =============================================

                        sqs.delete_message(
                            QueueUrl=self.queue,
                            ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" +
                              str(rekMessage['JobId']) +
                              ' : ' +
                              str(response['JobId']))

                    # Delete the unknown message
                    sqs.delete_message(
                        QueueUrl=self.queue,
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

        while finished is False:
            response = self.rek.get_label_detection(
                JobId=jobId,
                MaxResults=maxResults,
                NextToken=paginationToken,
                SortBy='TIMESTAMP')

            for labelDetection in response['Labels']:
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

        while finished is False:
            response = self.rek.get_person_tracking(
                JobId=jobId,
                MaxResults=maxResults,
                NextToken=paginationToken)

            for personDetection in response['Persons']:
                results.append(personDetection)

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

        return results

    # Gets the results of unsafe content label detection by calling
    # GetContentModeration.
    # Analysis is started by a call to StartContentModeration.
    # jobId is the identifier returned from StartContentModeration
    def GetResultsModerationLabels(self, jobId):
        maxResults = 500
        paginationToken = ''
        finished = False
        results = []

        while finished is False:
            response = self.rek.get_content_moderation(
                JobId=jobId,
                MaxResults=maxResults,
                NextToken=paginationToken)

            for contentModerationDetection in response['ModerationLabels']:
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

        while finished is False:
            response = self.rek.get_face_detection(
                JobId=jobId,
                MaxResults=maxResults,
                NextToken=paginationToken)

            for faceDetection in response['Faces']:
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

        while finished is False:
            response = self.rek.get_face_search(
                JobId=jobId,
                MaxResults=maxResults,
                NextToken=paginationToken)

            for personMatch in response['Persons']:
                results.append(personMatch)

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True
            print()

        return results

    # Gets the results of a celebrity detection analysis
    # by calling GetCelebrityRecognition.
    # Celebrity detection is started by calling StartCelebrityRecognition.
    # jobId is the identifier returned from StartCelebrityRecognition
    def GetResultsCelebrities(self, jobId):
        maxResults = 500
        paginationToken = ''
        finished = False
        results = []

        while finished is False:
            response = self.rek.get_celebrity_recognition(
                JobId=jobId,
                MaxResults=maxResults,
                NextToken=paginationToken)

            for celebrityRecognition in response['Celebrities']:
                results.append(celebrityRecognition)

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

        return results
