"""
State management module for tracking processed quiz URLs.

This module provides functionality to maintain a persistent record of processed
quiz URLs to prevent duplicate processing.

Supports both local file storage and online storage via GitHub Gist.
"""

import json
import os
import requests
from typing import Set, Optional
from pathlib import Path


class StateManager:
    """Manages the state of processed quiz URLs using local file and optional online storage."""
    
    def __init__(self, tracking_file: str = "data/scraped_urls.json", 
                 use_online: bool = True):
        """
        Initialize StateManager with tracking file path.
        
        Args:
            tracking_file: Path to the JSON file storing processed URLs
            use_online: Whether to use online storage (GitHub Gist)
        """
        self.tracking_file = tracking_file
        self.use_online = use_online
        self._processed_urls: Set[str] = set()
        
        # GitHub Gist configuration (optional)
        self.gist_token = os.getenv('GIST_TOKEN')
        self.gist_id = os.getenv('GIST_ID')
        
        # If online storage is enabled but not configured, fall back to local
        if self.use_online and (not self.gist_token or not self.gist_id):
            print("Warning: Online storage requested but GIST_TOKEN or GIST_ID not set.")
            print("Falling back to local file storage only.")
            self.use_online = False
        
    def _load_from_gist(self) -> Optional[Set[str]]:
        """
        Load processed URLs from GitHub Gist.
        
        Returns:
            Set of URLs or None if failed
        """
        if not self.use_online:
            return None
        
        try:
            headers = {
                'Authorization': f'token {self.gist_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(
                f'https://api.github.com/gists/{self.gist_id}',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                gist_data = response.json()
                # Get the first file in the gist
                files = gist_data.get('files', {})
                if files:
                    file_content = list(files.values())[0]['content']
                    data = json.loads(file_content)
                    urls = data.get("processed_urls", [])
                    print(f"Loaded {len(urls)} URLs from online storage")
                    return set(urls)
            else:
                print(f"Warning: Could not load from Gist (status {response.status_code})")
                return None
        except Exception as e:
            print(f"Warning: Could not load from online storage: {e}")
            return None
    
    def load_processed_urls(self) -> Set[str]:
        """
        Load the set of processed URLs from online storage or local file.
        
        Tries online storage first, falls back to local file.
        Creates the file with an empty list if it doesn't exist.
        
        Returns:
            Set of processed URLs
        """
        # Try online storage first
        if self.use_online:
            online_urls = self._load_from_gist()
            if online_urls is not None:
                self._processed_urls = online_urls
                # Also save to local file as backup
                self._save_to_local_file()
                return self._processed_urls
        
        # Fall back to local file
        tracking_path = Path(self.tracking_file)
        tracking_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create file if it doesn't exist
        if not tracking_path.exists():
            with open(self.tracking_file, 'w', encoding='utf-8') as f:
                json.dump({"processed_urls": []}, f, indent=2)
            self._processed_urls = set()
            return self._processed_urls
        
        # Load existing URLs from local file
        try:
            with open(self.tracking_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                urls = data.get("processed_urls", [])
                self._processed_urls = set(urls)
                return self._processed_urls
        except (json.JSONDecodeError, IOError) as e:
            # If file is corrupted, start fresh
            print(f"Warning: Could not load tracking file: {e}. Starting with empty state.")
            self._processed_urls = set()
            return self._processed_urls
    
    def is_processed(self, url: str) -> bool:
        """
        Check if a URL has been processed.
        
        Args:
            url: The quiz URL to check
            
        Returns:
            True if URL exists in processed set, False otherwise
        """
        return url in self._processed_urls
    
    def mark_processed(self, url: str) -> None:
        """
        Add URL to processed list and persist to storage.
        
        Args:
            url: The quiz URL to mark as processed
        """
        # Add to in-memory set
        self._processed_urls.add(url)
        
        # Persist to storage (online and local)
        self._save_to_file()
    
    def _save_to_local_file(self) -> None:
        """Save to local file only."""
        tracking_path = Path(self.tracking_file)
        tracking_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.tracking_file, 'w', encoding='utf-8') as f:
                data = {"processed_urls": sorted(list(self._processed_urls))}
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error: Could not save local tracking file: {e}")
    
    def _save_to_gist(self) -> bool:
        """
        Save processed URLs to GitHub Gist.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.use_online:
            return False
        
        try:
            headers = {
                'Authorization': f'token {self.gist_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            data = {"processed_urls": sorted(list(self._processed_urls))}
            content = json.dumps(data, indent=2, ensure_ascii=False)
            
            payload = {
                'files': {
                    'scraped_urls.json': {
                        'content': content
                    }
                }
            }
            
            response = requests.patch(
                f'https://api.github.com/gists/{self.gist_id}',
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print("Successfully saved to online storage")
                return True
            else:
                print(f"Warning: Could not save to Gist (status {response.status_code})")
                return False
        except Exception as e:
            print(f"Warning: Could not save to online storage: {e}")
            return False
    
    def _save_to_file(self) -> None:
        """
        Save the current state to both online and local storage.
        
        Internal method to persist the processed URLs set.
        """
        # Always save to local file as backup
        self._save_to_local_file()
        
        # Try to save to online storage if enabled
        if self.use_online:
            self._save_to_gist()
