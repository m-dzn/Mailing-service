import os
from google.oauth2 import service_account

from .settings import BASE_DIR

GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')
GS_PROJECT_ID = os.getenv('GS_PROJECT_ID')

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(os.path.join(BASE_DIR, 'credentials.json'))

# STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage' # static 파일들을 모두 Cloud Storage에 올릴 경우 설정
