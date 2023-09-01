#!/usr/bin/env python3
""" filtered logger module """
import logging
import re
import typing
from os import getenv
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: typing.List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ method to filter data """
    for f in fields:
        message = re.sub('{}=.+?{}'.format(f, separator),
                         '{}={}{}'.format(f, redaction, separator),
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: typing.List[str]):
        """ initialize method for class """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log records using filter_datum """
        s = filter_datum(self.fields, self.REDACTION,
                         super(RedactingFormatter, self).format(record),
                         self.SEPARATOR)
        return s


def get_logger() -> logging.Logger:
    """ logger method that returns a logging.Logger object """
    user_data = logging.getLogger('user_data')
    user_data.setLevel(logging.INFO)
    user_data.propagate = False
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter(PII_FIELDS))
    user_data.addHandler(sh)
    return user_data


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ connect to a secure holberton database to read a users table.
    The database is protected by a username and password that are set as
    environment variables on the server named PERSONAL_DATA_DB_USERNAME
    (set the default as “root”), PERSONAL_DATA_DB_PASSWORD
    and PERSONAL_DATA_DB_HOST (default as “localhost”).
    The database name is stored in PERSONAL_DATA_DB_NAME.
    Implement a get_db function that returns a connector to the database
    (mysql.connector.connection.MySQLConnection object).
    Use the os module to obtain credentials from the environment
    Use the module mysql-connector-python to connect to the MySQL database
    """
    mySql = mysql.connector.connection.MySQLConnection(
        user=getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=getenv('PERSONAL_DATA_DB_NAME'))
    return mySql


def main():
    '''
    main function that takes no arguments and
    returns nothing.
    '''
    database = get_db()
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]
    log = get_logger()
    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        log.info(str_row.strip())
    cursor.close()
    database.close()
