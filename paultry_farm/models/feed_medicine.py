"""
    Database Chicken feed models
"""
from paultry_farm.db.crud import open_db_connection
from paultry_farm.constants import Query
from paultry_farm import *


class Feed:

    @classmethod
    def add_feed(cls, feed_name):
        with open_db_connection('w') as db:
            db.execute(Query.FEED_INSERT_QUERY, feed_name=feed_name)
        logger.info('Added feed successfully: ' + feed_name)

    @classmethod
    def update_feed(cls, feed_name, new_feed_name):
        with open_db_connection('w') as db:
            db.execute(
                Query.FEED_UPDATE_QUERY,
                from_name=feed_name,
                to_name=new_feed_name
            )
        logger.info('Updated feed "{}" successfully to: {}'.format(feed_name, new_feed_name))

    @classmethod
    def delete_feed(cls, feed_name):
        with open_db_connection('w') as db:
            db.execute(Query.FEED_DELETE_QUERY, feed_name=feed_name)
        logger.info('Deleted feed successfully: ' + feed_name)

    @classmethod
    def get_all_feed(cls):
        with open_db_connection('w') as db:
            result_list = db.execute_get_all_rows(Query.FEED_GETALL_QUERY)

        result = [result_tuple[0] for result_tuple in result_list]
        logger.info('Fetched all feed names successfully!')
        return result


class Medicine:
    pass


if __name__ == '__main__':
    # Feed.add_feed('New feed')
    # # Feed.add_feed('duplicate2 food')
    # # Feed.add_feed('duplicate3 food')
    # # Feed.add_feed('duplicate4 food')
    # # Feed.add_feed('duplicate5 food')
    # # Feed.add_feed('duplicate6 food')
    # Feed.update_feed('New feed', 'proteins')
    # Feed.delete_feed('fish & craps')
    # Feed.delete_feed('duplicate food')
    for feed in Feed.get_all_feed():
        logger.info('Feed:' + feed)

# from paultry_farm import logger
# logger.info('This is sample text!')
# logger.info('This is sample text two!')
# logger.info('This is sample text two!')
# logger.debug('Just trying to debug so many words in the text input...!')
# logger.warn('Just trying to check if the warning message is printed correctly!')
