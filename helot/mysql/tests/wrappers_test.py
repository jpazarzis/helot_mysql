import csv
import os
import unittest
import unittest.mock as mock

from helot.common import configuration

from helot.mysql import db_connection
from helot.mysql import execute_query
from helot.mysql import make_non_query_executor
from helot.mysql import make_query_executor
from helot.mysql import query_executor_user

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
_RESOURCES_DIR = os.path.join(_CURRENT_DIR, 'resources')
_CONIFIGURATION_FILENAME = os.path.join(_RESOURCES_DIR, 'mysql.yaml')
_INVALID_CONIFIGURATION_FILENAME = os.path.join(_RESOURCES_DIR, 'invalid.yaml')
_WORLD_CAPITALS_FILENAME = os.path.join(_RESOURCES_DIR, 'world_capitals.csv')
_SQL_SELECT_CAPITALS = 'Select country, capital from world_capitals'
_SQL_DROP_DB = 'DROP Database If EXISTS {}'.format
_SQL_CREATE_DB = 'create Database {}'.format

_SQL_INSERT_CAPITAL = '''
Insert into world_capitals (
  country,
  capital
  )
values (
  '{country}',
  '{capital}'
)
'''.format

_SQL_CREATE_TABLE = '''
CREATE TABLE if not exists `world_capitals` (
  `country_id` int NOT NULL AUTO_INCREMENT,
  `country` varchar(128) DEFAULT NULL,
  `capital` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`country_id`)
)
'''

_CONIFIGURATION_FILENAME = {
    'mysql': {
        'host': 'localhost',
        'user': 'root',
        'passwd': 'vagrant',
        'db': 'test'
    }
}


class TestMysqlWrapper(unittest.TestCase):
    def setUp(self):
        configuration.initialize(_CONIFIGURATION_FILENAME)
        with make_non_query_executor(connect_to_db=False) as execute_query:
            db_name = configuration.mysql.db
            stmts = [
                _SQL_DROP_DB(db_name),
                _SQL_CREATE_DB(db_name),
            ]
            for sql in stmts:
                execute_query(sql)

        self.capitals = [
            (country, capital)
            for country, capital in csv.reader(open(_WORLD_CAPITALS_FILENAME))
        ]

        with make_non_query_executor() as execute_query:
            execute_query(_SQL_CREATE_TABLE)
            for country, capital in self.capitals:
                sql = _SQL_INSERT_CAPITAL(
                    country=country.replace("'", "''"),
                    capital=capital.replace("'", "''")
                )
                execute_query(sql)

    def test_make_query_executor(self):
        with make_query_executor() as execute_query:
            sql = _SQL_SELECT_CAPITALS
            retrieved = [
                (row.country, row.capital) for row in execute_query(sql)
            ]
            self.assertListEqual(retrieved, self.capitals)

    def test_execute_query(self):
        retrieved = []
        for row in execute_query(_SQL_SELECT_CAPITALS):
            retrieved.append((row.country, row.capital))
        self.assertListEqual(retrieved, self.capitals)

    @query_executor_user
    def test_execute_query_user(self, execute_query):
        sql = _SQL_SELECT_CAPITALS
        retrieved = [
            (row.country, row.capital) for row in execute_query(sql)
        ]
        self.assertListEqual(retrieved, self.capitals)

        # @mock.patch.object(mysql_wrapper, 'configuration')
        # @mock.patch.object(mysql_wrapper, 'MySQLdb')
        # def test_db_connection(self, mocked_MySQLdb, mocked_configuration):
        #     mocked_configuration.mysql.host = 'hst'
        #     mocked_configuration.mysql.user = 'usr'
        #     mocked_configuration.mysql.passwd = 'pwd'
        #     mocked_configuration.mysql.db = 'db'
        #
        #     params = {
        #         'host': 'hst',
        #         'user': 'usr',
        #         'passwd': 'pwd',
        #         'db': 'db'
        #     }
        #
        #     with db_connection():
        #         pass
        #
        #     mocked_MySQLdb.connect.assert_called_with(**params)
        #
        #     with db_connection(host='junk', user='junk', passwd='pwd', db='kk'):
        #         pass
        #
        #     params['host'] = 'junk'
        #     params['user'] = 'junk'
        #     params['passwd'] = 'pwd'
        #     params['db'] = 'kk'
        #     mocked_MySQLdb.connect.assert_called_with(**params)
