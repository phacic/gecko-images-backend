from api.main import app


def test_home(client):
    resp = client.get("/")

    assert resp.status_code == 200


class TestUploadImage:

    def test_upload_image_upload(self, client, create_jpg_image):
        """ test upload allowed image extension """

        with open(create_jpg_image.name, 'rb') as im:
            data = {
                "file": im
            }

            resp = client.post("/upload_image", data=data, content_type="multipart/form-data")
            assert resp.status_code == 200
            assert resp.json['image_id'] is not None

    def test_upload_not_allowed_image(self, client, create_tiff_image):
        with open(create_tiff_image.name, 'rb') as im:
            data = {
                "file": im
            }

            resp = client.post("/upload_image", data=data, content_type="multipart/form-data")
            assert resp.status_code == 400

    def test_upload_a_link(self, client):
        pass


class TestAnalyseImage:

    def test_with_non_existing_image(self, client):
        url = "/analyse_image?image_id=12345"
        resp = client.get(url)
        assert resp.status_code == 404

    def test_without_image_id(self, client):
        url = "/analyse_image"
        resp = client.get(url)
        assert resp.status_code == 400

    def test_with_existing_image(self, client, create_jpg_image):
        # upload a file
        image_id = None
        with open(create_jpg_image.name, 'rb') as im:
            data = {
                "file": im
            }

            resp = client.post("/upload_image", data=data, content_type="multipart/form-data")
            assert resp.status_code == 200
            image_id = resp.json['image_id']

        # analyse
        url = f"/analyse_image?image_id={image_id}"
        resp = client.get(url)
        assert resp.status_code == 200
        assert resp.json['width'] is not None
        assert resp.json['height'] is not None
