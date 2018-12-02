from video_face_detection import VideoDetect


def get_results():
    analyzer = VideoDetect()
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

    return person_analysis_results


def video_analyze():
    analyzer = VideoDetect()
    face_analysis_results = analyzer.main(task='face_detection')
    person_analysis_results = analyzer.main(task='person_tracking')
    return merge_results(face_analysis_results, person_analysis_results)


def merge_results(face_analysis_results, person_analysis_results):
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
            timestamp = str(faceDetection['Timestamp'])
            face_bounding_box_left = faceDetection['Face']['BoundingBox']['Left']

            if timestamp in face_timestamp_dict and face_bounding_box_left == face_timestamp_dict[timestamp]['BoundingBox']['Left']:
                personsWithFaces[index][timestamp] = faceDetection['Face']

    return personsWithFaces
    