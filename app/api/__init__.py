from flask import Blueprint
from . import video, music, books, processor

video_bp = Blueprint('video', __name__)
music_bp = Blueprint('music', __name__)
books_bp = Blueprint('books', __name__)
processor_bp = Blueprint('processor', __name__)