# Standard library imports
import os
from typing import List

# Third-party imports
from sqlalchemy import create_engine, text
from sqlalchemy.engine.row import Row
from sqlalchemy.exc import DBAPIError
from dotenv import load_dotenv

load_dotenv()


class DbManager(object):
    """
    Helper class to establish connections to Postgres and
    run queries. Queries are run loading text files from
    a given directory containing SQL statements.

    Example:
        db = DbManager(db_uri=os.getenv('DATABASE_URI'), query_dir='sql')
        db.run_query('insert_instructor.sql')
    """

    def __init__(
        self,
        db_uri: str,
        query_dir: str,
        debug: bool = False,
    ) -> None:
        """
        Args:
            db_uri: Database URI
            query_dir: Location of queries
            debug: Whether or not logging should be enabled
        """
        self.query_dir = query_dir
        self.engine = create_engine(db_uri, echo=debug, echo_pool='debug' if debug else False)

    def _load_query(self, query_name: str) -> str:
        """
        Loads query expression from file

        Args:
            query_name: Name of the text file containing query

        Returns:
            Query expression string
        """

        with open(os.path.join(self.query_dir, query_name)) as f:
            query_string = ''.join(f.readlines())

        return query_string

    def _execute(self, query: str, params: dict = None) -> List[Row]:
        """
        Executes SQL expression

        Args:
            query: Text of the query
            params: Optional query parameters
        """

        try:
            if params:
                result = self.conn.execute(text(query), params)
            else:
                result = self.conn.execute(text(query))

            if result.returns_rows:
                return result.fetchall()
            else:
                return []
        except DBAPIError as e:
            print(f'DBAPIError: {e.orig}')
            return []

    def open_conn(self):
        self.conn = self.engine.connect()

    def close_conn(self):
        self.conn.close()

    def run_query(self, query_name: str, params: dict = None) -> List[Row]:
        """
        Executes query expression from text file

        Args:
            query_name: Name of the text file containing query
            params: Optional query parameters
        """
        query_expr = self._load_query(query_name)
        return self._execute(query=query_expr, params=params)
