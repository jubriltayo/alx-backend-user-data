#!/usr/bin/env python3
"""This module encrypts personal data"""
import re
from typing import List
import logging
from os import environ
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """obscure/redact return message"""
    for word in fields:
        message = re.sub(f"{word}=.*?{separator}",
                         f"{word}={redaction}{separator}",
                         message
                         )
    return message


def get_logger() -> logging.Logger:
    """returns a logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to a MYSQL database"""
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    connector = mysql.connector.connection.MySQLConnection(
        user=username, password=password, host=host, database=db_name
    )
    return connector


def main():
    """obtain a database connection using get_db and retrieve all rows
        in the users table and display each row under a filtered format
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [desc[0] for desc in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f"{f}={str(r)}; " for r, f in zip(row, field_names))
        logger.info(str_row.strip())
    
    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR
                                  )
        return super(RedactingFormatter, self).format(record)


if __name__ == "__main__":
    main()