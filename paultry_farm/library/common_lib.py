from paultry_farm import logger
from json import dumps


def is_data_type(data, data_type, tuple_size=None):
    if data_type is 'list_of_tuple':

        if not len(data):
            raise Exception('No elements are present in data: {}. Unable to determine datatype!'.format(data))

        if type(data) is list and type(data[0]) is tuple:
            logger.info('Data is of type: ' + data_type)

            if tuple_size is not None and not all(len(_tuple) == tuple_size for _tuple in data):
                return False

            return True

        logger.error('Data is not of type: ' + data_type)
        return False

    return type(data) is data_type


def pretty_print(data, message=None, indent=2):
    print_data = dumps(data, indent=indent)

    msg = '\n'
    if message is not None:
        msg = message + msg

    logger.info(msg + print_data)
