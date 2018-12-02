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

for faceDetection in face_analysis_results:
    for index, face_timestamp_dict in personsWithFaces.items():
        face_timestamp = faceDetection['Timestamp']
        face_bounding_box = faceDetection['Face']['BoundingBox']

        if (timestamp in face_timestamp_dict and
                face_bounding_box['Left'] == face_timestamp_dict[timestamp]['BoundingBox']['Left']):
            personsWithFaces[index][timestamp] = faceDetection['Face']

print(json.dumps(personsWithFaces))
