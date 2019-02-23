"""
    Database Chicken feed models
"""
from paultry_farm.db.crud import open_db_connection
from paultry_farm.constants import Query


class Feed:

    @classmethod
    def add_feed(cls, feed_name):
        with open_db_connection('w') as db:
            db.execute(Query.FEED_INSERT_QUERY, feed_name=feed_name)
        # TODO: log

    @classmethod
    def update_feed(cls, feed_name, new_feed_name):
        with open_db_connection('w') as db:
            db.execute(
                Query.FEED_UPDATE_QUERY,
                from_name=feed_name,
                to_name=new_feed_name
            )

        # TODO: log

    @classmethod
    def delete_feed(cls, feed_name):
        with open_db_connection('w') as db:
            db.execute(Query.FEED_DELETE_QUERY, feed_name=feed_name)
        # TODO: log

    @classmethod
    def get_all_feed(cls):
        with open_db_connection('w') as db:
            result_list = db.execute_get_all_rows(Query.FEED_GETALL_QUERY)

        result = [result_tuple[0] for result_tuple in result_list]
        # TODO: log
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
    Feed.delete_feed('fish & craps')
    # for feed in Feed.get_all_feed():
    #     print('Feed:', feed)
