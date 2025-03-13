"""PostgreSQL database connection management."""

import os
import logging
from typing import Dict, Any
from contextlib import contextmanager
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor

from business_assistant.config.settings import settings

logger = logging.getLogger(__name__)

# Connection pool for PostgreSQL
_pool = None


def get_connection_pool():
    """Get or create the database connection pool.

    Returns:
        SimpleConnectionPool: The connection pool instance.
    """
    global _pool
    if _pool is None:
        try:
            _pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=settings.db_host,
                port=settings.db_port,
                dbname=settings.db_name,
                user=settings.db_user,
                password=settings.db_password,
            )
            logger.info("Database connection pool created successfully")
        except Exception as e:
            logger.error(f"Error creating database connection pool: {str(e)}")
            raise
    return _pool


@contextmanager
def get_db_connection():
    """Get a database connection from the pool.

    Yields:
        connection: A database connection from the pool.
    """
    pool = get_connection_pool()
    connection = None
    try:
        connection = pool.getconn()
        yield connection
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise
    finally:
        if connection:
            pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    """Get a database cursor from a connection in the pool.

    Args:
        commit (bool): Whether to commit the transaction after operations.

    Yields:
        cursor: A database cursor for executing queries.
    """
    with get_db_connection() as connection:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                connection.commit()
        except Exception as e:
            connection.rollback()
            logger.error(f"Database operation error: {str(e)}")
            raise
        finally:
            cursor.close()


def execute_query(query: str, params: Dict[str, Any] = None, commit: bool = False):
    """Execute a database query and return results.

    Args:
        query (str): SQL query to execute.
        params (Dict[str, Any], optional): Query parameters. Defaults to None.
        commit (bool, optional): Whether to commit the transaction. Defaults to False.

    Returns:
        list: Query results as a list of dictionaries.
    """
    with get_db_cursor(commit=commit) as cursor:
        cursor.execute(query, params or {})
        if cursor.description:
            return cursor.fetchall()
        return None


def execute_many(query: str, params_list: list, commit: bool = True):
    """Execute a query with multiple parameter sets.

    Args:
        query (str): SQL query to execute.
        params_list (list): List of parameter dictionaries.
        commit (bool, optional): Whether to commit the transaction. Defaults to True.

    Returns:
        bool: True if successful.
    """
    with get_db_cursor(commit=commit) as cursor:
        cursor.executemany(query, params_list)
    return True
