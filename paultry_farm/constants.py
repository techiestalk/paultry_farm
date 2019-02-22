import os

__DB_FILE = '../datastore.db'
DATABASE_PATH = os.path.abspath(__DB_FILE)


class Query:
    FEED_INSERT_QUERY = 'INSERT INTO FEED(FEED_NAME) VALUES("{feed_name}")'
    FEED_UPDATE_QUERY = 'UPDATE FEED SET FEED_NAME="{to_name}" where FEED_NAME="{from_name}"'
    FEED_DELETE_QUERY = 'DELETE FROM FEED WHERE FEED_NAME="{feed_name}";'
    FEED_GETALL_QUERY = 'SELECT FEED_NAME FROM FEED ORDER BY FEED_NAME;'
