import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME') or 'tracker_app_db'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key-that_cannot-be-guessedWAAAA'
    TRACKER_PER_PAGE = os.environ.get('TRACKER_PER_PAGE') or 20
    PROJECTS_PER_PAGE = os.environ.get('TRACKER_PER_PAGE') or 20
    ALLOWED_EXTENSIONS = set(['torrent'])
  
