
"""
Cache manager module for managing data cache
Author: Prof. V. Ravichandran
"""

import os
import pickle
import pandas as pd
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any, Optional


class CacheManager:
    """Manage caching of fetched data"""

    def __init__(self, cache_dir: str = ".cache", cache_duration_hours: int = 24):
        """
        Initialize CacheManager
        
        Args:
            cache_dir: Directory to store cache files
            cache_duration_hours: How long to keep cache (hours)
        """
        self.cache_dir = cache_dir
        self.cache_duration_hours = cache_duration_hours
        self.cache_file = os.path.join(cache_dir, "data_cache.pkl")
        
        # Create cache directory if it doesn't exist
        try:
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create cache directory: {str(e)}")

    def save_cache(self, data: Dict, metadata: Optional[Dict] = None) -> bool:
        """
        Save data to cache
        
        Args:
            data: Data to cache
            metadata: Additional metadata
            
        Returns:
            True if successful
        """
        try:
            cache_data = {
                'data': data,
                'timestamp': datetime.now(),
                'metadata': metadata or {}
            }
            
            # Ensure directory exists
            os.makedirs(self.cache_dir, exist_ok=True)
            
            with open(self.cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            
            return True
        except Exception as e:
            print(f"Error saving cache: {str(e)}")
            return False

    def load_cache(self) -> Tuple[Optional[Dict], bool, Dict]:
        """
        Load data from cache
        
        Returns:
            Tuple of (data, is_valid, cache_info)
        """
        try:
            if not os.path.exists(self.cache_file):
                return None, False, {}
            
            with open(self.cache_file, 'rb') as f:
                cache_data = pickle.load(f)
            
            # Check if cache is still valid
            cached_at = cache_data.get('timestamp')
            if cached_at:
                age_hours = (datetime.now() - cached_at).total_seconds() / 3600
                is_valid = age_hours < self.cache_duration_hours
            else:
                is_valid = False
            
            cache_info = {
                'cached_at': str(cached_at) if cached_at else 'Unknown',
                'age_hours': age_hours if cached_at else 0,
                'rows': len(cache_data.get('data', {}))
            }
            
            data = cache_data.get('data')
            return data, is_valid, cache_info
            
        except Exception as e:
            print(f"Error loading cache: {str(e)}")
            return None, False, {}

    def clear_cache(self) -> bool:
        """
        Clear cache
        
        Returns:
            True if successful
        """
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
            return True
        except Exception as e:
            print(f"Error clearing cache: {str(e)}")
            return False

    def get_cache_info(self) -> Dict:
        """
        Get cache information
        
        Returns:
            Dictionary with cache info
        """
        try:
            if not os.path.exists(self.cache_file):
                return {'exists': False}
            
            with open(self.cache_file, 'rb') as f:
                cache_data = pickle.load(f)
            
            cached_at = cache_data.get('timestamp')
            age_hours = (datetime.now() - cached_at).total_seconds() / 3600 if cached_at else 0
            
            return {
                'exists': True,
                'cached_at': str(cached_at) if cached_at else 'Unknown',
                'age_hours': age_hours,
                'rows': len(cache_data.get('data', {})),
                'age_info': {
                    'cached_at': str(cached_at) if cached_at else 'Unknown',
                    'age_hours': int(age_hours),
                    'time_remaining_hours': max(0, int(self.cache_duration_hours - age_hours))
                }
            }
        except Exception as e:
            print(f"Error getting cache info: {str(e)}")
            return {'exists': False}
