# Seu projeto/storage_backends.py (Exemplo: church_site/storage_backends.py)

from storages.backends.s3boto3 import S3ManifestStaticStorage

class R2StaticStorage(S3ManifestStaticStorage):
    # O bucket (media) e o prefixo (static) já estão definidos 
    # nas variáveis AWS_STORAGE_BUCKET_NAME e AWS_LOCATION do settings.py
    pass