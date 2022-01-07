from typing import Generator
import tempfile
import pytest
from PIL import Image
from flask.testing import FlaskClient
from api.main import app


@pytest.fixture(scope='session', autouse=True)
def create_temp_photos_dir() -> Generator:
    # setup
    photos_temp_dir = tempfile.TemporaryDirectory()

    # replace upload folder
    app.config["UPLOADS_FULL_PATH"] = photos_temp_dir.name
    yield photos_temp_dir.name

    # tear down
    photos_temp_dir.cleanup()


@pytest.fixture()
def client() -> Generator[FlaskClient, None, None]:
    yield app.test_client()


@pytest.fixture()
def create_jpg_image():
    """ jpeg image file factory """
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tf:
        image = Image.new("RGB", (100, 100), color="#ddd")
        image.save(tf, format="JPEG")
        tf.close()

    yield tf

    # clean up
    image.close()


@pytest.fixture()
def create_tiff_image():
    """ jpeg image file factory """
    with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as tf:
        image = Image.new("RGB", (100, 100), color="#ddd")
        image.save(tf, format="TIFF")
        tf.close()

    yield tf

    # clean up
    image.close()
