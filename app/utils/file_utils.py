import io
import zipfile


def convert_files_into_zip(file_list):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for filename, file in file_list:
            zip_file.writestr(filename, file)

    buffer.seek(0)
    return buffer
