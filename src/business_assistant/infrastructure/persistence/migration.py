"""Database migration module for the Business Assistant application."""
import logging
from typing import List, Tuple, Optional

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from business_assistant.config.settings import settings
from business_assistant.infrastructure.persistence.queries.conversation_queries import (
    CREATE_CONVERSATIONS_TABLE,
    CREATE_MESSAGES_TABLE,
    CREATE_CONVERSATION_INDEXES,
)
from business_assistant.infrastructure.persistence.queries.products_queries import (
    CREATE_CATEGORIES_TABLE,
    CREATE_PRODUCTS_TABLE,
    CREATE_PRODUCT_VARIANTS_TABLE,
    CREATE_INVENTORY_TABLE,
    CREATE_PRODUCT_INDEXES,
)

logger = logging.getLogger(__name__)


class DatabaseMigration:
    """Database migration manager for the Business Assistant application."""

    def __init__(self):
        """Initialize the database migration manager."""
        self.settings = settings
        
    def check_database_exists(self) -> bool:
        """Check if the database exists.
        
        Returns:
            bool: True if the database exists, False otherwise.
            
        Raises:
            Exception: If there's an error connecting to the database server.
        """
        try:
            # Try to connect to the database
            conn = psycopg2.connect(
                host=self.settings.db_host,
                port=self.settings.db_port,
                user=self.settings.db_user,
                password=self.settings.db_password,
                database=self.settings.db_name
            )
            conn.close()
            logger.info(f"Database {self.settings.db_name} exists")
            return True
        except psycopg2.OperationalError as e:
            if f"database \"{self.settings.db_name}\" does not exist" in str(e):
                logger.error(f"Database {self.settings.db_name} does not exist. Please create it using the setup_db.py script.")
                return False
            # Re-raise other connection errors
            logger.error(f"Error connecting to database: {str(e)}")
            raise
    
    def migrate(self) -> bool:
        """Run database migrations to ensure all tables and indexes exist.
        
        Returns:
            bool: True if migrations were applied successfully, False otherwise.
            
        Raises:
            Exception: If the database doesn't exist or there's an error connecting to it.
        """
        # First check if the database exists
        if not self.check_database_exists():
            raise Exception(f"Database '{self.settings.db_name}' does not exist. Please run the setup_db.py script first.")
            
        try:
            # Connect to the business assistant database
            conn = psycopg2.connect(
                host=self.settings.db_host,
                port=self.settings.db_port,
                dbname=self.settings.db_name,
                user=self.settings.db_user,
                password=self.settings.db_password,
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Run migrations
            migrations = self._get_migrations()
            
            for name, query in migrations:
                logger.info(f"Running migration: {name}")
                cursor.execute(query)
            
            cursor.close()
            conn.close()
            logger.info("Database migrations completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error running migrations: {str(e)}")
            return False
    
    def _get_migrations(self) -> List[Tuple[str, str]]:
        """Get all migrations to be applied.
        
        Returns:
            List[Tuple[str, str]]: List of tuples containing (migration_name, sql_query)
        """
        return [
            # Conversation tables
            ("Create conversations table", CREATE_CONVERSATIONS_TABLE),
            ("Create messages table", CREATE_MESSAGES_TABLE),
            ("Create conversation indexes", CREATE_CONVERSATION_INDEXES),
            
            # Product tables
            ("Create categories table", CREATE_CATEGORIES_TABLE),
            ("Create products table", CREATE_PRODUCTS_TABLE),
            ("Create product variants table", CREATE_PRODUCT_VARIANTS_TABLE),
            ("Create inventory table", CREATE_INVENTORY_TABLE),
            ("Create product indexes", CREATE_PRODUCT_INDEXES),
        ]


def run_migrations() -> bool:
    """Run all database migrations.
    
    Returns:
        bool: True if migrations were applied successfully, False otherwise.
    """
    migration = DatabaseMigration()
    return migration.migrate()
