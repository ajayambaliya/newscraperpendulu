"""
Unit tests for StateManager module.

Tests cover:
- Loading empty and existing tracking files
- URL checking and marking as processed
- File persistence
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.state_manager import StateManager


class TestStateManager(unittest.TestCase):
    """Test cases for StateManager class."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_urls.json")
        self.state_manager = StateManager(tracking_file=self.test_file)
    
    def tearDown(self):
        """Clean up test fixtures after each test."""
        # Remove test files and directory
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
    
    def test_load_empty_tracking_file(self):
        """Test loading when tracking file doesn't exist."""
        # File should not exist initially
        self.assertFalse(os.path.exists(self.test_file))
        
        # Load should create empty file
        processed_urls = self.state_manager.load_processed_urls()
        
        # Should return empty set
        self.assertEqual(len(processed_urls), 0)
        self.assertIsInstance(processed_urls, set)
        
        # File should now exist
        self.assertTrue(os.path.exists(self.test_file))
        
        # File should contain empty list
        with open(self.test_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data, {"processed_urls": []})
    
    def test_load_existing_tracking_file(self):
        """Test loading when tracking file exists with URLs."""
        # Create file with sample URLs
        sample_urls = [
            "https://example.com/quiz1",
            "https://example.com/quiz2",
            "https://example.com/quiz3"
        ]
        
        with open(self.test_file, 'w') as f:
            json.dump({"processed_urls": sample_urls}, f)
        
        # Load URLs
        processed_urls = self.state_manager.load_processed_urls()
        
        # Should return set with all URLs
        self.assertEqual(len(processed_urls), 3)
        self.assertIsInstance(processed_urls, set)
        self.assertEqual(processed_urls, set(sample_urls))
    
    def test_is_processed_returns_false_for_new_url(self):
        """Test that is_processed returns False for unprocessed URLs."""
        # Load empty state
        self.state_manager.load_processed_urls()
        
        # Check new URL
        result = self.state_manager.is_processed("https://example.com/new-quiz")
        
        self.assertFalse(result)
    
    def test_is_processed_returns_true_for_existing_url(self):
        """Test that is_processed returns True for processed URLs."""
        # Create file with sample URL
        test_url = "https://example.com/quiz1"
        
        with open(self.test_file, 'w') as f:
            json.dump({"processed_urls": [test_url]}, f)
        
        # Load URLs
        self.state_manager.load_processed_urls()
        
        # Check existing URL
        result = self.state_manager.is_processed(test_url)
        
        self.assertTrue(result)
    
    def test_mark_processed_adds_url(self):
        """Test that mark_processed adds URL to the set."""
        # Load empty state
        self.state_manager.load_processed_urls()
        
        test_url = "https://example.com/new-quiz"
        
        # URL should not be processed initially
        self.assertFalse(self.state_manager.is_processed(test_url))
        
        # Mark as processed
        self.state_manager.mark_processed(test_url)
        
        # URL should now be processed
        self.assertTrue(self.state_manager.is_processed(test_url))
    
    def test_mark_processed_persists_to_file(self):
        """Test that mark_processed saves URL to file."""
        # Load empty state
        self.state_manager.load_processed_urls()
        
        test_url = "https://example.com/new-quiz"
        
        # Mark as processed
        self.state_manager.mark_processed(test_url)
        
        # Read file directly
        with open(self.test_file, 'r') as f:
            data = json.load(f)
        
        # URL should be in file
        self.assertIn(test_url, data["processed_urls"])
    
    def test_mark_processed_multiple_urls(self):
        """Test marking multiple URLs as processed."""
        # Load empty state
        self.state_manager.load_processed_urls()
        
        test_urls = [
            "https://example.com/quiz1",
            "https://example.com/quiz2",
            "https://example.com/quiz3"
        ]
        
        # Mark all as processed
        for url in test_urls:
            self.state_manager.mark_processed(url)
        
        # All should be processed
        for url in test_urls:
            self.assertTrue(self.state_manager.is_processed(url))
        
        # Read file directly
        with open(self.test_file, 'r') as f:
            data = json.load(f)
        
        # All URLs should be in file
        self.assertEqual(len(data["processed_urls"]), 3)
        for url in test_urls:
            self.assertIn(url, data["processed_urls"])
    
    def test_mark_processed_duplicate_url(self):
        """Test that marking same URL twice doesn't create duplicates."""
        # Load empty state
        self.state_manager.load_processed_urls()
        
        test_url = "https://example.com/quiz1"
        
        # Mark as processed twice
        self.state_manager.mark_processed(test_url)
        self.state_manager.mark_processed(test_url)
        
        # Read file directly
        with open(self.test_file, 'r') as f:
            data = json.load(f)
        
        # Should only appear once
        self.assertEqual(data["processed_urls"].count(test_url), 1)
    
    def test_file_persistence_across_instances(self):
        """Test that state persists across different StateManager instances."""
        # Load empty state
        self.state_manager.load_processed_urls()
        
        test_url = "https://example.com/quiz1"
        
        # Mark as processed
        self.state_manager.mark_processed(test_url)
        
        # Create new instance with same file
        new_state_manager = StateManager(tracking_file=self.test_file)
        new_state_manager.load_processed_urls()
        
        # URL should be processed in new instance
        self.assertTrue(new_state_manager.is_processed(test_url))


if __name__ == '__main__':
    unittest.main()
