from video_face_detection import VideoDetect

def video_analyze():
    analyzer = VideoDetect()
    face_analysis_results = analyzer.main(task='face_detection')
    person_analysis_results = analyzer.main(task='person_tracking')

    personsWithFaces = {}

    for personDetection in person_analysis_results:
        if 'Face' in personDetection['Person']:
            index = str(personDetection['Person']['Index'])
            timestamp = str(personDetection['Timestamp'])

            if index not in personsWithFaces:
                personsWithFaces[index] = {}

            personsWithFaces[index][timestamp] = personDetection['Person']['Face']

    for faceDetection in face_analysis_results:
        for index, face_timestamp_dict in personsWithFaces.items():
            timestamp = faceDetection['Timestamp']
            face_bounding_box_left = faceDetection['Face']['BoundingBox']['Left']

            if timestamp in face_timestamp_dict and face_bounding_box_left == face_timestamp_dict[timestamp]['BoundingBox']['Left']:
                personsWithFaces[index][timestamp] = faceDetection['Face']

    return personsWithFaces


        


