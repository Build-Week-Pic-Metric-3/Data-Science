from decouple import config
from werkzeug.utils import secure_filename
import boto3, botocore

S3_BUCKET = config('S3_BUCKET')
S3_KEY = config('S3_KEY')
S3_SECRET = config('S3_SECRET')
bucket_name = S3_BUCKET

S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

s3 = boto3.client(
   "s3",
   aws_access_key_id= S3_KEY,
   aws_secret_access_key= S3_SECRET
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(S3_LOCATION, file.filename)