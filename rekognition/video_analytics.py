from video_face_detection import VideoDetect
import configparser
from pymongo import MongoClient
from datetime import datetime, date, time


class VideoAnalytics:

    def __init__(self, configPath, video, videoStartTime):
        self.video = video
        self.videoStartTime = videoStartTime
        config = configparser.ConfigParser()
        config.read(configPath)
        configDefaultSection = config['DEFAULT']
        self.queue = configDefaultSection['queue']
        self.roleArn = configDefaultSection['roleArn']
        self.topicArn = configDefaultSection['topicArn']
        self.bucket = configDefaultSection['bucket']
        self.results = []
        self.mongoClient = MongoClient(configDefaultSection['mongoDbUrl'])
        self.storeDatabase = self.mongoClient[configDefaultSection['storeName']]
        self.storeCollection = self.storeDatabase[configDefaultSection['storeLocation']]

    def CollectResults(self):
        analyzer = VideoDetect(
            self.queue,
            self.roleArn,
            self.topicArn,
            self.bucket,
            self.video)

        face_analysis_results = analyzer.main(task='face_detection')
        person_analysis_results = analyzer.main(task='person_tracking')

        timestamp_to_face_dict = {}
        for faceDetection in face_analysis_results:
            timestamp = str(faceDetection['Timestamp'])

            if timestamp not in timestamp_to_face_dict:
                timestamp_to_face_dict[timestamp] = {}

            timestamp_to_face_dict[timestamp][faceDetection['Face']['BoundingBox']['Left']] = faceDetection['Face']

        for personDetection in person_analysis_results:
            if 'Face' in personDetection['Person']:
                timestamp = str(personDetection['Timestamp'])
                face_bounding_box_left = personDetection['Person']['Face']['BoundingBox']['Left']

                if timestamp in timestamp_to_face_dict and face_bounding_box_left in timestamp_to_face_dict[timestamp]:
                    personDetection['Person']['Face'] = timestamp_to_face_dict[timestamp][face_bounding_box_left]

        self.results = person_analysis_results

    def AddResultsToDatabase(self):
        for result in self.results:
            result['Timestamp'] = int(self.videoStartTime.timestamp() * 1000) + int(result['Timestamp'])
            self.storeCollection.insert_one(result)

if __name__ == "__main__":
    videoAnalytics = VideoAnalytics(
        '../settings.ini',
        '1201181734.mp4',
        datetime.now())
    videoAnalytics.CollectResults()
    videoAnalytics.AddResultsToDatabase()
