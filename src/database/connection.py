"""
Database connection utilities for the Aika AI System.
"""

import os
from typing import Any, Dict, Optional

from supabase import Client, create_client

from ..utils.config import get_settings
from ..utils.logging import get_logger

# Get logger
logger = get_logger(__name__)

# Get settings
settings = get_settings()

# Supabase client instance
_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """
    Get the Supabase client instance.
    
    Returns:
        Supabase client
    """
    global _supabase_client
    
    if _supabase_client is None:
        try:
            url = settings.SUPABASE_URL
            key = settings.SUPABASE_SERVICE_KEY
            
            logger.info("Initializing Supabase client")
            _supabase_client = create_client(url, key)
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise
    
    return _supabase_client


def execute_query(
    table: str, 
    query_type: str = "select", 
    columns: str = "*", 
    filters: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = None,
    order: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute a query on the specified table.
    
    Args:
        table: Table name
        query_type: Query type (select, insert, update, delete)
        columns: Columns to select
        filters: Query filters
        limit: Result limit
        order: Order by clause
        
    Returns:
        Query result
    """
    client = get_supabase_client()
    
    try:
        if query_type == "select":
            query = client.table(table).select(columns)
            
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            if order:
                query = query.order(order)
                
            if limit:
                query = query.limit(limit)
                
            return query.execute()
        else:
            # Other query types will be implemented as needed
            raise NotImplementedError(f"Query type '{query_type}' not implemented")
    except Exception as e:
        logger.error(f"Database query error: {e}")
        raise
