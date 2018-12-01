import boto3

# BUCKET = 'dv-ai-hacks'
# KEY = 'test3.jpg'

def detect_faces(bucket, key, attributes=['ALL'], region='us-west-2'):
    '''
    Returns the AWS Rekognition detect_faces() response on an image stored in an S3 bucket. 
    '''
    rekognition = boto3.client('rekognition', region)
    response = rekognition.detect_faces(
        Image = {
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        Attributes = attributes,
    ) 
    return response['FaceDetails']

def create_face_collection(collection_id, region='us-west-2'):
    client = boto3.client('rekognition', region)
    existing_collections = client.list_collections()['CollectionIds']

    if collection_id in existing_collections:
        return None
    else:
        client.create_collection(CollectionId=collection_id)


IMAGE_ID = KEY # S3 key is the image id.
COLLECTION = 'customers-collection'

def index_faces(bucket, key, collection_id, image_id=None, attributes = (), region='us-west-2'):
    '''
    Detects faces in the input image and adds them to the specified collection.
    A collection must be created first through the use of the create_face_collection function.
    
    Amazon Rekognition doesn't save the actual faces that are detected.
    Instead, the underlying detection algorithm first detects the faces in the input image. 
    For each face, the algorithm extracts facial features into a feature vector, and stores it in the backend database. 
    Amazon Rekognition uses feature vectors when it performs face match and search operations using the SearchFaces 
    and SearchFacesByImage operations.
    '''
    rekognition = boto3.client('rekognition', region)
    response = rekognition.index_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        },
        CollectionId = collection_id,
        ExternalImageId = image_id,
        DetectionAttributes = attributes,
    )
    return response['FaceRecords']
