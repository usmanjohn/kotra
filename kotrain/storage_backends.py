from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    default_acl = None


class StaticStorage(S3Boto3Storage):
    location = 'static'  # This is the folder name in your S3 bucket
    default_acl = None  # Or 'None' if your bucket does not support ACLs
    file_overwrite = False