import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_EXTENSIONS = ['.jpg', '.png', '.gif']
UPLOAD_DIR = 'photos'
UPLOADS_FULL_PATH = os.path.join(BASE_DIR, UPLOAD_DIR)
