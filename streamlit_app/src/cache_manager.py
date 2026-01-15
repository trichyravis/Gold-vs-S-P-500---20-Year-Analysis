"""
Cache Manager Module - Smart caching with auto-refresh functionality
Author: Prof. V. Ravichandran
"""

import os
import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple, Dict
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """Manage data caching with expiration and auto-refresh"""
    
    def __init__(self, cache_dir: str, cache_duration_hours: int = 24):
        """
        Initialize CacheManager
        
        Args:
            cache_dir: Directory for cache files
            cache_duration_hours: Hours before cache expires
        """
        self.cache_dir = cache_dir
        self.cache_duration_hours = cache_duration_hours
        
        # Create cache directory if it doesn't exist
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        
        self.metadata_file = os.path.join(cache_dir, 'cache_metadata.json')
        self.csv_cache = os.path.join(cache_dir, 'data_cache.csv')
        self.parquet_cache = os.path.join(cache_dir, 'data_cache.parquet')
    
    def save_cache(self, df: pd.DataFrame, metadata: Dict = None) -> bool:
        """
        Save data to cache
        
        Args:
            df: DataFrame to cache
            metadata: Optional metadata dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Save to both CSV and Parquet for flexibility
            df.to_csv(self.csv_cache, index=False)
            df.to_parquet(self.parquet_cache, index=False)
            
            # Save metadata
            cache_metadata = {
                'cached_at': datetime.now().isoformat(),
                'rows': len(df),
                'columns': list(df.columns),
                'start_date': str(df['date'].min()) if 'date' in df.columns else None,
                'end_date': str(df['date'].max()) if 'date' in df.columns else None,
                'cache_duration_hours': self.cache_duration_hours,
                'expires_at': (datetime.now() + timedelta(hours=self.cache_duration_hours)).isoformat()
            }
            
            # Merge with provided metadata
            if metadata:
                cache_metadata.update(metadata)
            
            with open(self.metadata_file, 'w') as f:
                json.dump(cache_metadata, f, indent=2)
            
            logger.info(f"✅ Cache saved successfully at {datetime.now()}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving cache: {str(e)}")
            return False
    
    def load_cache(self) -> Tuple[Optional[pd.DataFrame], bool, Dict]:
        """
        Load data from cache if valid
        
        Args:
            None
            
        Returns:
            Tuple of (DataFrame or None, is_valid, metadata)
        """
        metadata = {}
        
        try:
            # Check if cache files exist
            if not os.path.exists(self.parquet_cache):
                return None, False, {'reason': 'No cache file found'}
            
            if not os.path.exists(self.metadata_file):
                return None, False, {'reason': 'No cache metadata found'}
            
            # Load metadata
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
            
            # Check if cache is expired
            if not self.is_cache_valid(metadata):
                return None, False, {'reason': 'Cache expired'}
            
            # Load data from parquet (faster)
            df = pd.read_parquet(self.parquet_cache)
            
            # Ensure date is datetime
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            logger.info(f"✅ Cache loaded successfully ({len(df)} rows)")
            return df, True, metadata
            
        except Exception as e:
            logger.error(f"❌ Error loading cache: {str(e)}")
            return None, False, {'reason': f'Error loading cache: {str(e)}'}
    
    def is_cache_valid(self, metadata: Dict = None) -> bool:
        """
        Check if cache is still valid (not expired)
        
        Args:
            metadata: Cache metadata dictionary
            
        Returns:
            True if cache is valid, False otherwise
        """
        if metadata is None:
            try:
                with open(self.metadata_file, 'r') as f:
                    metadata = json.load(f)
            except:
                return False
        
        try:
            # Check expiration
            expires_at = datetime.fromisoformat(metadata.get('expires_at', ''))
            is_valid = datetime.now() < expires_at
            
            if is_valid:
                logger.info(f"✅ Cache is valid (expires: {metadata.get('expires_at')})")
            else:
                logger.info(f"⚠️ Cache expired (expired at: {metadata.get('expires_at')})")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"❌ Error checking cache validity: {str(e)}")
            return False
    
    def get_cache_age(self, metadata: Dict = None) -> Optional[Dict]:
        """
        Get cache age information
        
        Args:
            metadata: Cache metadata dictionary
            
        Returns:
            Dictionary with age information or None
        """
        if metadata is None:
            try:
                with open(self.metadata_file, 'r') as f:
                    metadata = json.load(f)
            except:
                return None
        
        try:
            cached_at = datetime.fromisoformat(metadata.get('cached_at', ''))
            expires_at = datetime.fromisoformat(metadata.get('expires_at', ''))
            now = datetime.now()
            
            age = now - cached_at
            time_remaining = expires_at - now
            
            return {
                'cached_at': cached_at.strftime('%Y-%m-%d %H:%M:%S'),
                'age_seconds': int(age.total_seconds()),
                'age_minutes': int(age.total_seconds() / 60),
                'age_hours': int(age.total_seconds() / 3600),
                'expires_at': expires_at.strftime('%Y-%m-%d %H:%M:%S'),
                'time_remaining_seconds': max(0, int(time_remaining.total_seconds())),
                'time_remaining_hours': max(0, int(time_remaining.total_seconds() / 3600)),
                'is_valid': now < expires_at
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting cache age: {str(e)}")
            return None
    
    def clear_cache(self) -> bool:
        """
        Clear all cached data
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(self.csv_cache):
                os.remove(self.csv_cache)
            
            if os.path.exists(self.parquet_cache):
                os.remove(self.parquet_cache)
            
            if os.path.exists(self.metadata_file):
                os.remove(self.metadata_file)
            
            logger.info("✅ Cache cleared successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error clearing cache: {str(e)}")
            return False
    
    def get_cache_info(self) -> Dict:
        """
        Get information about current cache
        
        Returns:
            Dictionary with cache information
        """
        try:
            if not os.path.exists(self.metadata_file):
                return {
                    'exists': False,
                    'message': 'No cache found'
                }
            
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
            
            cache_age = self.get_cache_age(metadata)
            
            return {
                'exists': True,
                'rows': metadata.get('rows', 0),
                'columns': metadata.get('columns', []),
                'start_date': metadata.get('start_date'),
                'end_date': metadata.get('end_date'),
                'cached_at': metadata.get('cached_at'),
                'expires_at': metadata.get('expires_at'),
                'cache_duration_hours': metadata.get('cache_duration_hours'),
                'is_valid': self.is_cache_valid(metadata),
                'age_info': cache_age
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting cache info: {str(e)}")
            return {
                'exists': False,
                'error': str(e)
            }
    
    def export_data(self, df: pd.DataFrame, format: str = 'csv', filepath: str = None) -> Tuple[bool, str]:
        """
        Export data to various formats
        
        Args:
            df: DataFrame to export
            format: Export format ('csv', 'excel', 'parquet')
            filepath: Optional custom filepath
            
        Returns:
            Tuple of (success, filepath or error message)
        """
        try:
            if filepath is None:
                ext = {
                    'csv': '.csv',
                    'excel': '.xlsx',
                    'parquet': '.parquet'
                }.get(format, '.csv')
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filepath = os.path.join(self.cache_dir, f'export_{timestamp}{ext}')
            
            if format == 'csv':
                df.to_csv(filepath, index=False)
            elif format == 'excel':
                df.to_excel(filepath, index=False, engine='openpyxl')
            elif format == 'parquet':
                df.to_parquet(filepath, index=False)
            else:
                return False, f"Unsupported format: {format}"
            
            logger.info(f"✅ Data exported to {filepath}")
            return True, filepath
            
        except Exception as e:
            logger.error(f"❌ Error exporting data: {str(e)}")
            return False, str(e)
