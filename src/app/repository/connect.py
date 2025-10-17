# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
import pyodbc
from google.auth import default
from google.cloud import firestore
from app.config import config
import logger_config
import os


logger = logger_config.get_logger(__name__)


def connect():
    """
    Connect to the database. This function has been updated to work with Google Cloud services.
    For now, it provides a basic SQL connection without Azure AD dependencies.
    """
    logger.info(f'Connecting to database...')
    
    # For development/testing, we'll use a simple connection without authentication
    # In production, you would set up Google Cloud SQL with proper authentication
    
    # For development, return a mock connection or None
    logger.info('Using development mode - no actual database connection')
    return None


def get_firestore_client():
    """
    Get a Firestore client for document storage (alternative to SQL for some use cases)
    """
    try:
        # Set up Google Cloud credentials if project ID is provided
        if config.gcp_project_id and config.gcp_project_id != 'placeholder-project':
            os.environ['GOOGLE_CLOUD_PROJECT'] = config.gcp_project_id
            
        # Initialize Firestore client
        db = firestore.Client(
            project=config.gcp_project_id if config.gcp_project_id != 'placeholder-project' else None,
            database=config.firestore_database_id
        )
        logger.info('Connected to Firestore')
        return db
    except Exception as e:
        logger.warning(f'Failed to connect to Firestore: {e}')
        return None
