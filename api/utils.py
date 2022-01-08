import os
from typing import Tuple, Union
from uuid import uuid4
from PIL import Image
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import requests

from api.constants import (ALLOWED_EXTENSIONS, UPLOADS_FULL_PATH, BASE_DIR)


def gen_filename() -> str:
    """
    create a filename using uuid.
    :return: filename as string
    """
    return secure_filename(uuid4().hex)


def get_file_ext(filename: str) -> str:
    """
    retrieve file extension if any
    :return: extension as string
    """
    return os.path.splitext(filename)[1]


def validate_ext(filename: str) -> bool:
    """ validate file extension is allowed """

    ext = get_file_ext(filename)
    return ext in ALLOWED_EXTENSIONS


def save_uploaded_image(file: FileStorage) -> str:
    """ save image and return image id (filename without extension) """
    from api.main import app

    # create photos folder if it doesn't exist
    upload_path = app.config['UPLOADS_FULL_PATH']
    os.makedirs(upload_path, exist_ok=True)

    ext = get_file_ext(file.filename)
    filename = gen_filename()
    filename_ext = f"{filename}{ext}"
    path = os.path.join(upload_path, filename_ext)
    file.save(path)

    return filename


def save_image_from_url(url: str) -> Union[str, None]:
    """ download and save image from url and return image id (filename without extension) """
    from api.main import app

    # create photos folder if it doesn't exist
    upload_path = app.config['UPLOADS_FULL_PATH']
    os.makedirs(upload_path, exist_ok=True)

    ext = get_file_ext(url)
    filename = gen_filename()
    filename_ext = f"{filename}{ext}"
    path = os.path.join(upload_path, filename_ext)

    # download file
    resp = requests.get(url, headers={"Accept": "*/*"})
    if resp.status_code == 200:
        with open(path, 'wb') as f:
            f.write(resp.content)
            return filename

    # return error status code
    return None


def get_image_detail(image_id: str) -> Union[Tuple, None]:
    """ get image height and width if exists"""
    from api.main import app

    path = app.config['UPLOADS_FULL_PATH']
    image_list = os.listdir(path)
    for image in image_list:
        if image.split(".")[0] == image_id:
            image_path = os.path.join(path, image)
            im = Image.open(image_path)
            width, height = im.size
            return width, height

    return None
