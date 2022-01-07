import os
from typing import Tuple, Union
from uuid import uuid4
from PIL import Image
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


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
    os.makedirs(UPLOADS_FULL_PATH, exist_ok=True)

    ext = get_file_ext(file.filename)
    filename = gen_filename()
    filename_ext = f"{filename}{ext}"
    path = os.path.join(app.config['UPLOADS_FULL_PATH'], filename_ext)
    file.save(path)

    return filename


def image_exist(image_id: str) -> bool:
    """ check if image with filename exists """
    # to get around cyclic import
    from api.main import app

    path = app.config['UPLOADS_FULL_PATH']
    image_list = os.listdir(path)

    return any(image.split(".")[0] == image_id for image in image_list)


def get_image_detail(image_id: str) -> Union[Tuple, None]:
    """ get image height and width if exists"""
    from api.main import app

    if image_exist(image_id):
        path = app.config['UPLOADS_FULL_PATH']
        image_list = os.listdir(path)
        for image in image_list:
            if image.split(".")[0] == image_id:
                image_path = os.path.join(path, image)
                im = Image.open(image_path)
                width, height = im.size
                return width, height

    return None

