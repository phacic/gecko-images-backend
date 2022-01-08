# Images backend

## Running server
Docker needs to be installed to run the server. Run the following command to start the server

```shell
docker-compose up -d
```

The server is accessible on `http://localhost:5005/`

## Endpoints
Endpoint supported, more details in `image.postman_collection.json`

### Upload image
_POST_ `http://localhost:5005/upload_image`

Accepts an image file, or a source url for the image, save the uploaded image and returns a unique `image_id`

### Analyse image
_GET_ `http://localhost:5005/upload_image?image_id={}`

Returns the width and height for corresponding `image_id`

### List images
_GET_ `http://localhost:5005/list_images`

List all images with their unique image_id

## Testing
Run the following to run unit tests.

```shell
docker-compose run --rm web pytest -v
```