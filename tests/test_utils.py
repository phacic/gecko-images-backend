import uuid
from api.utils import gen_filename, get_file_ext


def test_gen_filename():
    """test generated filenames"""

    name = gen_filename()
    assert uuid.UUID(name)


def test_get_file_ext():
    """"""
    name = "file.jpg"

    ext = get_file_ext(name)
    assert ext == ".jpg"

    name = "file"
    ext = get_file_ext(name)

    assert ext == ""

