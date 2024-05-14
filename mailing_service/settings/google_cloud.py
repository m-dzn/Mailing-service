import os
from google.oauth2 import service_account

from .settings import BASE_DIR

GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID')

STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(os.path.join(BASE_DIR, 'credentials.json'))
