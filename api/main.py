import json
import os

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from api.utils import (
    validate_ext, save_uploaded_image, get_image_detail, save_image_from_url
)
from api.constants import (
    ALLOWED_EXTENSIONS, UPLOAD_DIR, UPLOADS_FULL_PATH
)

app = Flask(__name__)

# apply COR
CORS(app)

# configuration =====

# allowed image extensions
app.config['UPLOAD_EXTENSIONS'] = ALLOWED_EXTENSIONS

# max image size (2MB). Will be automatically evaluated
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 2

# upload dir
app.config['UPLOAD_PATH'] = UPLOAD_DIR
app.config['UPLOADS_FULL_PATH'] = UPLOADS_FULL_PATH


# ===================

@app.route("/")
def home():
    return jsonify({"message": "welcome to image uploader"})


@app.route("/upload_image", methods=["POST"])
def upload_image():
    """ upload an image using either the image file or a url to the image"""
    if request.files.get("file"):
        uploaded_file = request.files['file']

        # validate file extension
        if not validate_ext(uploaded_file.filename):
            # could be better with json response
            abort(400, "File not allowed.")

        # save uploaded image
        image_id = save_uploaded_image(uploaded_file)
        return jsonify({"image_id": image_id})

    elif request.is_json:
        # if file not uploaded we can assume image url upload
        request_data = request.json

        image_url = request_data.get("url")
        if not validate_ext(image_url):
            abort(400, "File not allowed.")

        image_id = save_image_from_url(image_url)
        if not image_id:
            abort(400, "Image download failed.")
        return jsonify({"image_id": image_id})

    # no file upload or image url, abort
    abort(400)


@app.route("/analyse_image", methods=["GET"])
def analyse_image():
    image_id = request.args.get("image_id")

    # image_id should be provided
    if not image_id:
        abort(400, "image_id not provided")

    detail = get_image_detail(image_id)
    if detail:
        width, height = detail
        return jsonify({'height': height, 'width': width, 'image_id': image_id})
    else:
        abort(404, "image does not exist")


@app.route("/list_images", methods=["GET"])
def list_images():
    image_list = os.listdir(app.config['UPLOADS_FULL_PATH'])
    ret_list = []
    for image in image_list:
        ret_list.append({
            "id": image.split(".")[0],
            "image": os.path.join(app.config['UPLOAD_PATH'], image)
        })
    return jsonify(ret_list)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
