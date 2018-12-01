import boto3

BUCKET = "storefront-analytics"
KEY = "IMG_3950.png"
FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")

def detect_faces(bucket, key, attributes=['ALL'], region="us-west-2"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.detect_faces(
        Image={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": key,}
        },
        Attributes=attributes,
    )
    return response['FaceDetails']