import os

# Project constants/
PROJECT_HOME_PATH = os.path.abspath('..')

# Database Constants
__DB_FILE = '../datastore.db'
DATABASE_PATH = os.path.abspath(__DB_FILE)

# Logger constants
LOG_DIR = os.path.abspath(os.path.join(PROJECT_HOME_PATH, '../../logs'))
APP_LOG_PATH = os.path.join(LOG_DIR, 'app_log.log')
LOG_FORMATTER = '%(asctime)s [%(filename)18s:%(lineno)3s] %(levelname)5s - %(message)s'
LOG_TIME_FMT = '%Y-%m-%d %H:%M:%S'


# Query constants
class Query:
    FEED_INSERT_QUERY = 'INSERT INTO FEED(FEED_NAME) VALUES(:feed_name)'
    FEED_UPDATE_QUERY = 'UPDATE FEED SET FEED_NAME= :to_name where FEED_NAME=:from_name'
    FEED_DELETE_QUERY = 'DELETE FROM FEED WHERE FEED_NAME=":feed_name";'
    FEED_GETALL_QUERY = 'SELECT FEED_NAME FROM FEED ORDER BY FEED_NAME;'
