import pandas as pd

from abc import ABC, abstractmethod

from django.db import connections
from django.db.models.query import QuerySet


class PandasQueryABC(ABC):

    @abstractmethod
    def _get_connection(self, db_name: str):
        """
        Return django connection, default db_name = 'default'.
        """

    @abstractmethod
    def _pandas_query(self) -> pd.DataFrame:
        """
        Return DataFrame after sql query have executed.
        """

    @abstractmethod
    def get_dataframe(self) -> pd.DataFrame:
        """
        Return dataframe after execution method _pandas_query
        """


class PandasQuery(PandasQueryABC):
    DEFAULT_DB_NAME = 'default'

    __slots__ = ['query', 'db_name']
    __dict__ = ['_get_connection', '_pandas_query', 'get_dataframe']

    def __init__(self, query, db_name: str = DEFAULT_DB_NAME):
        self.query: str = str(query.query) if type(query) is QuerySet else query
        self.db_name: str = db_name

    def _get_connection(self, db_name: str = DEFAULT_DB_NAME):
        return connections[db_name]

    def _pandas_query(self) -> pd.DataFrame:
        return pd.read_sql(self.query,
                           self._get_connection(self.db_name),
                           coerce_float=True)

    def get_dataframe(self) -> pd.DataFrame:
        return self._pandas_query()
