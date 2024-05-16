import os
from uuid import uuid4
from storages.backends.gcloud import GoogleCloudStorage

storage = GoogleCloudStorage()


def upload_file(file, directory):
    try:
        original_filename = file.name

        uuid = uuid4()
        parts = file.name.rsplit('.', 1)
        if len(parts) == 2:
            extension = parts[1]
        else:
            extension = ''

        filename_to_store = f'{uuid}.{extension}'
        target_path = f'{directory}/{filename_to_store}'
        path = storage.save(target_path, file)

        return {
            'file_path': storage.url(path),
            'original_filename': original_filename,
            'stored_filename': filename_to_store,
            'extension': extension,
            'file_size': file.size,
        }
    except Exception as e:
        raise e


def get_file(filename, directory):
    file_path = get_file_path(filename, directory)

    bucket = storage.client.bucket(os.getenv('GS_BUCKET_NAME'))
    blob = bucket.blob(file_path)

    return blob.download_as_bytes()


def get_file_path(filename, directory):
    return (f'{directory}/' if directory is not None else '') + filename


def remove_file(filename, directory):
    file_path = (f'{directory}/' if directory is not None else '') + filename

    if storage.exists(file_path):
        storage.delete(file_path)
        print(f'{file_path} has been deleted.')
    else:
        print(f'{file_path} does not exist.')
