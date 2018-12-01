import boto3

# BUCKET = 'dv-ai-hacks'
# KEY = 'test3.jpg'

def detect_faces(bucket, key, attributes=['ALL'], region="us-west-2"):
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