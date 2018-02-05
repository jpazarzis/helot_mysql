"""Mysql wrappers to execute mysql statements.
The default behaviour depends on the configuration module which contains the
database settings to use.
"""

from contextlib import contextmanager
from functools import wraps
import logging

import MySQLdb
from helot_common import configuration


@contextmanager
def db_connection(host=None, user=None, passwd=None, db=None,
                  connect_to_db=True):
    """Auto closing db connection context manager.
    Yields an active db connection which will be closed automatically.
    :parameter connect_to_db: (boolean) True to connect to the database.
    Otherwise it will no connect to a specific database, something that can be
    useful in the case of a database creation.
    """
    params = {
        'host': host or configuration.mysql.host,
        'user': user or configuration.mysql.user,
        'passwd': passwd or configuration.mysql.passwd
    }

    if connect_to_db:
        params['db'] = db or configuration.mysql.db

    db_conn = MySQLdb.connect(**params)
    yield db_conn
    db_conn.close()


@contextmanager
def db_cursor(db_conn):
    """Auto closing db cursor context manager.
    Yields an live db cursor which will be closed automatically.
    :parameter db_conn: The db connection to use for the creation of the cursor.
    """
    cur = db_conn.cursor()
    yield cur
    cur.close()


@contextmanager
def make_query_executor(*args, **kwargs):
    """Context manager providing a function to execute sql queries.
    Yields a query executor function.
    """
    with db_connection(*args, **kwargs) as db_conn, db_cursor(db_conn) as cur:
        def execute_query(sql):
            cur.execute(sql)
            col_names = [col_data[0] for col_data in cur.description]
            for row in cur.fetchall():
                row_data = _RawData()
                for i, cell in enumerate(row):
                    setattr(row_data, col_names[i], cell)
                yield row_data

        yield execute_query


@contextmanager
def make_non_query_executor(*args, **kwargs):
    """Context manager providing a function to execute non query statements.
    Yields a non query executor function.
    :parameter use_db: (boolean) True to connect to the database. Otherwise it
    will no connect to a specific database, something that can be useful in the
    case of a database creation.
    """
    with db_connection(*args, **kwargs) as db_conn, db_cursor(db_conn) as cur:
        def execute_non_query(sql):
            try:
                cur.execute(sql)
                db_conn.commit()
            except Exception as ex:
                logging.exception(ex)
                db_conn.rollback()

        yield execute_non_query


class _RawData(object):
    """Used to create the object to encapsulate the data of retrieved row."""


def query_executor_user(function_to_decorate):
    """Decorates a function adding an execute query function argument.
    When decorates a function its signature must contain an argument called
    execute_query which will receive a sql executor to use for queries.
    :parameter  function_to_decorate: The function to decorate.
    :returns : The decorated function containing the execute_query argument.
    """

    @wraps(function_to_decorate)
    def decorator(*args, **kargs):
        with make_query_executor() as execute_query:
            kargs['execute_query'] = execute_query
            return function_to_decorate(*args, **kargs)

    return decorator


def execute_query(sql, **kwargs):
    """Simplest way to execute a query.
    Opens and closes a new connection and cursor every time called.
    :param sql:  (str) The sql statement to execute.
    :param kwargs: The connection settings.
    Yields a sequence of rows coming from the execution of the query.
    """
    with make_query_executor(**kwargs) as executor:
        for row in executor(sql):
            yield row
