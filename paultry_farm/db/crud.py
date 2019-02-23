"""
    Database CRUD utility
"""
from paultry_farm.constants import DATABASE_PATH
from paultry_farm import *
import sqlite3


class Database:

    def __init__(self, query_type='r'):
        self.connection = None
        self.cursor = None
        self.query_type = query_type

    def __enter__(self):
        if self.connection is None:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()
        logger.info('DB Connection is successful')

    def execute(self, query, **kwargs):
        """
            Executes the given insert row, update row or create table query.
            The method does not return results.

            @param      query       SQL query string
            @param      data
            @return     None
        """
        if self.connection is None:
            raise Exception('Database has to be connected first to execute query')

        try:
            self.cursor.execute(query, kwargs)
            if self.query_type in ('w', 'write'):
                self.connection.commit()
            logger.info('Query executed successfully: ' + query)
        except Exception as e:
            logger.error('Failed to execute query: {}\nCaused by: {}'.format(query, e))
            raise

    def execute_get_row(self, query):
        """
            Executes the given query and fetch one row of result
            The method does not return results.

            @param      query       SQL query string
            @return     tuple       Result as one row
        """
        if self.connection is None:
            raise Exception('Database has to be connected first to execute query')

        try:
            self.cursor.execute(query)
            return_val = self.cursor.fetchone()
            logger.info('Query executed successfully: ' + query)
        except Exception as e:
            logger.error('Failed to execute query: {}\nCaused by: {}'.format(query, e))
            raise

        return return_val

    def execute_get_all_rows(self, query):
        """
            Executes the given query and fetch all results as list of tuples

            @param      query           SQL query string
            @return     list(tuples)    Result set as set of tuples
        """
        if self.connection is None:
            raise Exception('Database has to be connected first to execute query')

        try:
            self.cursor.execute(query)
            return_val = self.cursor.fetchall()
            logger.info('Query executed successfully: ' + query)
        except Exception as e:
            logger.error('Failed to execute query: {}\nCaused by: {}'.format(query, e))
            raise

        return return_val

    def close(self):
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()
            logger.info('DB Connection is closed!')


open_db_connection = Database

if __name__ == '__main__':
    # # Test drop tables
    # table = 'FEED'
    # drop = 'DROP TABLE ' + table
    # with open_db_connection('w') as db:
    #     db.execute(drop)
    #     print("Table dropped: " + table)

    # # # Test create tables
    # with Database() as db:
    #     create_1 = "create table FEED(" \
    #                "FEED_ID INTEGER PRIMARY KEY AUTOINCREMENT, " \
    #                "FEED_NAME CHAR(50) NOT NULL, " \
    #                "UNIQUE (FEED_NAME)" \
    #                ");"
    #     db.execute(create_1)

    # get_feed_query = 'select * from FEED where FEED_NAME like "VEG%";'
    get_feed_query = "select DISTINCT(FEED_NAME) from FEED"

    with open_db_connection('write') as db:
        result_list = db.execute_get_all_rows(get_feed_query)

    for result in result_list:
        feed_name = result[0]
        logger.info('Feed Name:' + feed_name)
