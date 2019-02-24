"""
    Database CRUD utility
"""
from paultry_farm.constants import DATABASE_PATH, Query
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
            logger.info('Executing query: ' + query)
            self.cursor.execute(query, kwargs)
            if self.query_type in ('w', 'write'):
                self.connection.commit()
            logger.info('Query executed successfully!')
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

    def get_values(self, table_name, *columns, **kwargs):
        """
            Executes the given query and fetch all results as list of tuples

            @param      table_name      Name of the table to query
            @param      columns         Result columns
            @param      kwargs          Identifier to locate row
            @return     list(tuples)    Result set as set of tuples
            @example
                with open_db_connection() as db:
                    result = db.get_values('test1', 'pay', 'name', identifier='address', id_value='chennai')
                    logger.info(result)

            @log
                2019-02-24 16:14:23 [crud.py: 27]  INFO - DB Connection is successful
                2019-02-24 16:14:23 [crud.py:126]  INFO - Executing query: SELECT pay,name FROM test1 WHERE address = :id_value;
                2019-02-24 16:14:23 [crud.py:164]  INFO - [(1000, 'user_1'), (2000, 'user_2'), (3000, 'user_3')]
                2019-02-24 16:14:23 [crud.py:148]  INFO - DB Connection is closed!
        """
        if self.connection is None:
            raise Exception('Database has to be connected first to execute query')

        query = str()

        try:
            # Build columns to query for
            if not columns:
                select_columns = '*'
            else:
                select_columns = ','.join(columns)

            # Form select query
            if kwargs:
                query = Query.TABLE_GET_QUERY.format(
                    columns=select_columns,
                    table=table_name,
                    identifier=kwargs['identifier']
                )
            else:
                query = Query.TABLE_GETALL_QUERY.format(
                    columns=select_columns,
                    table=table_name
                )

            logger.info('Executing query: ' + query)
            if kwargs:
                logger.info('Query arguments: {}'.format(kwargs))

            self.cursor.execute(query, kwargs)
            return_val = self.cursor.fetchall()

            # Convert list of tuples with one element to list of strings
            if is_data_type(return_val, 'list_of_tuple', tuple_size=1):
                return_val = [_tuple[0] for _tuple in return_val if len(_tuple) == 1]

            # Convert singular data from tuple to string
            if type(return_val) is list and len(return_val) == 1:
                return return_val[0]

        except Exception as e:
            logger.error('Failed to fetch fields "{}" from table: {}\nCaused by: {}'
                         .format(columns, table_name, e))
            raise

        return return_val

    def insert_row(self, table_name, **kwargs):
        """
            Executes the given query to insert a row in a table

            @param      table_name      Name of the table to query
            @param      kwargs          Column names with values
            @return                     None (success), Exception (failure)

            @example
                with open_db_connection() as db:
                     db.insert_row('test1', name='user_5', pay=1000, address='chennai')

            @log
                2019-02-24 18:16:23 [crud.py: 27]  INFO - DB Connection is successful
                2019-02-24 18:16:23 [crud.py:185]  INFO - Executing query: INSERT INTO test1 (pay, name, address) VALUES (:pay, :name, :address);
                2019-02-24 18:16:23 [crud.py:187]  INFO - Query arguments: {'pay': 1000, 'name': 'user_5', 'address': 'chennai'}
                2019-02-24 18:16:23 [crud.py:204]  INFO - DB Connection is closed!

        """
        if self.connection is None:
            raise Exception('Database has to be connected first to execute query')

        keys = kwargs.keys()
        query = 'INSERT INTO {table_name} ('.format(table_name=table_name)
        columns = ', '.join([str(key) for key in keys])
        values = ', '.join([':' + str(key) for key in keys])
        query += columns + ') VALUES ('
        query += values + ');'

        try:
            logger.info('Executing query: ' + query)
            if kwargs:
                logger.info('Query arguments: {}'.format(kwargs))

            self.cursor.execute(query, kwargs)
            self.connection.commit()
        except sqlite3.IntegrityError:
            logger.error('Value "{}" already exists in table. Skipping ...'.format(list(kwargs.values())))

        except Exception as e:
            logger.error('Failed to insert fields "{}" to table: {}\nCaused by: {}'
                         .format(columns, table_name, e))
            raise

    def close(self):
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()
            logger.info('DB Connection is closed!')


open_db_connection = Database

if __name__ == '__main__':
    with open_db_connection() as db:
        db.insert_row('test1', name='user_5', pay=1000, address='chennai')

    # with open_db_connection() as db:
    #     # rows = db.get_values('feed', 'feed_name')
    #     result = db.get_values('test1', 'pay', 'name', identifier='address', id_value='chennai')
    #     # result = db.get_values('test1', 'pay', 'name')
    #     logger.info(result)
    #
    #     result = db.get_values('test1')
    #     logger.info(result)
    #
    #     result = db.get_values('test1', 'pay', 'name')
    #     logger.info(result)
    #
    #     # Negative case
    #     result = db.get_values('test2', 'pay', 'name1')
    #     logger.info(result)

    # # Test drop tables
    # table = 'FEED'
    # drop = 'DROP TABLE ' + table
    # with open_db_connection('w') as db:
    #     db.execute(drop)
    #     print("Table dropped: " + table)

    # # Test create tables
    # with Database() as db:
    #     create_1 = "create table TEST1(" \
    #                "ID INTEGER PRIMARY KEY AUTOINCREMENT, " \
    #                "NAME CHAR(50) NOT NULL, " \
    #                "PAY INTEGER NOT NULL, " \
    #                "ADDRESS CHAR(50) NOT NULL," \
    #                " UNIQUE (NAME)" \
    #                ");"
    #     db.execute(create_1)

    # # get_feed_query = 'select * from FEED where FEED_NAME like "VEG%";'
    # get_feed_query = "select DISTINCT(FEED_NAME) from FEED"
    #
    # with open_db_connection('write') as db:
    #     result_list = db.execute_get_all_rows(get_feed_query)
    #
    # for result in result_list:
    #     feed_name = result[0]
    #     logger.info('Feed Name:' + feed_name)
