from storages.backends.s3boto3 import S3Boto3Storage

class R2StaticStorage(S3Boto3Storage):
    location = "static"               # garante caminho correto
    default_acl = "public-read"
    file_overwrite = True
    custom_domain = "pub-ba1a1273b7274c32ada11ba5a4254e40.r2.dev"
