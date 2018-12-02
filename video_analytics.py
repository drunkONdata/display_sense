from neha.video_face_detection import VideoDetect
from collections import defaultdict
import json

analyzer = VideoDetect()
face_analysis_results = analyzer.main(task='face_detection')
person_analysis_results = analyzer.main(task='person_tracking')

personsWithFaces = {}

for personDetection in person_analysis_results:
    if 'Face' in personDetection['Person']:
        index = personDetection['Person']['Index']
        timestamp = personDetection['Timestamp']

        if index not in personsWithFaces:
            personsWithFaces[index] = {}

        personsWithFaces[index][timestamp] = personDetection['Person']['Face']

        print('Index: ' + str(personDetection['Person']['Index']))
        print('Timestamp: ' + str(personDetection['Timestamp']))
        print()

for faceDetection in face_analysis_results:
    for index, face_timestamp_dict in personsWithFaces.items():
        face_timestamp = faceDetection['Timestamp']
        face_bounding_box = faceDetection['Face']['BoundingBox']
        person_bounding_box = face_timestamp_dict[timestamp]['BoundingBox']

        if (timestamp in face_timestamp_dict and
                face_bounding_box['Left'] == person_bounding_box['Left']):
            personsWithFaces[index][timestamp] = faceDetection['Face']

print(json.dumps(personsWithFaces))
