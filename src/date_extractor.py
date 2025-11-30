"""
Date extraction utility for quiz URLs
Handles various date formats in pendulumedu.com URLs
"""

import re
from datetime import datetime
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DateExtractor:
    """Extract dates from quiz URLs in various formats"""
    
    # Month name mappings
    MONTH_MAP = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    
    # Gujarati month names
    GUJARATI_MONTHS = {
        1: 'જાન્યુઆરી', 2: 'ફેબ્રુઆરી', 3: 'માર્ચ', 4: 'એપ્રિલ',
        5: 'મે', 6: 'જૂન', 7: 'જુલાઈ', 8: 'ઓગસ્ટ',
        9: 'સપ્ટેમ્બર', 10: 'ઓક્ટોબર', 11: 'નવેમ્બર', 12: 'ડિસેમ્બર'
    }
    
    def __init__(self):
        """Initialize date extractor with regex patterns"""
        # Pattern 1: "28-november-2025" or "28-nov-2025"
        self.pattern1 = re.compile(
            r'(\d{1,2})-([a-z]+)-(\d{4})',
            re.IGNORECASE
        )
        
        # Pattern 2: "23-and-24-november-2025" (date range)
        self.pattern2 = re.compile(
            r'(\d{1,2})-and-(\d{1,2})-([a-z]+)-(\d{4})',
            re.IGNORECASE
        )
        
        # Pattern 3: "28-11-2025" (numeric format)
        self.pattern3 = re.compile(
            r'(\d{1,2})-(\d{1,2})-(\d{4})'
        )
        
        # Pattern 4: "november-28-2025" (month first)
        self.pattern4 = re.compile(
            r'([a-z]+)-(\d{1,2})-(\d{4})',
            re.IGNORECASE
        )
    
    def extract_date_from_url(self, url: str) -> Optional[Tuple[datetime, str, str]]:
        """
        Extract date from quiz URL.
        
        Args:
            url: Quiz URL
            
        Returns:
            Tuple of (datetime object, formatted date string, gujarati date string)
            or None if no date found
        """
        logger.info(f"Extracting date from URL: {url}")
        
        # Try pattern 2 first (date range)
        match = self.pattern2.search(url)
        if match:
            day1 = int(match.group(1))
            day2 = int(match.group(2))
            month_name = match.group(3).lower()
            year = int(match.group(4))
            
            month = self._parse_month(month_name)
            if month:
                # Use the first date for datetime object
                date_obj = datetime(year, month, day1)
                
                # Format: "23 and 24 November 2025"
                formatted = f"{day1} and {day2} {month_name.capitalize()} {year}"
                
                # Gujarati: "23 અને 24 નવેમ્બર 2025"
                gujarati = f"{day1} અને {day2} {self.GUJARATI_MONTHS[month]} {year}"
                
                logger.info(f"✓ Extracted date range: {formatted}")
                return (date_obj, formatted, gujarati)
        
        # Try pattern 1 (single date with month name)
        match = self.pattern1.search(url)
        if match:
            day = int(match.group(1))
            month_name = match.group(2).lower()
            year = int(match.group(3))
            
            month = self._parse_month(month_name)
            if month:
                date_obj = datetime(year, month, day)
                
                # Format: "28 November 2025"
                formatted = f"{day} {month_name.capitalize()} {year}"
                
                # Gujarati: "28 નવેમ્બર 2025"
                gujarati = f"{day} {self.GUJARATI_MONTHS[month]} {year}"
                
                logger.info(f"✓ Extracted date: {formatted}")
                return (date_obj, formatted, gujarati)
        
        # Try pattern 4 (month first)
        match = self.pattern4.search(url)
        if match:
            month_name = match.group(1).lower()
            day = int(match.group(2))
            year = int(match.group(3))
            
            month = self._parse_month(month_name)
            if month:
                date_obj = datetime(year, month, day)
                
                # Format: "28 November 2025"
                formatted = f"{day} {month_name.capitalize()} {year}"
                
                # Gujarati: "28 નવેમ્બર 2025"
                gujarati = f"{day} {self.GUJARATI_MONTHS[month]} {year}"
                
                logger.info(f"✓ Extracted date: {formatted}")
                return (date_obj, formatted, gujarati)
        
        # Try pattern 3 (numeric format)
        match = self.pattern3.search(url)
        if match:
            day = int(match.group(1))
            month = int(match.group(2))
            year = int(match.group(3))
            
            if 1 <= month <= 12 and 1 <= day <= 31:
                try:
                    date_obj = datetime(year, month, day)
                    
                    # Format: "28 November 2025"
                    month_name = date_obj.strftime("%B")
                    formatted = f"{day} {month_name} {year}"
                    
                    # Gujarati: "28 નવેમ્બર 2025"
                    gujarati = f"{day} {self.GUJARATI_MONTHS[month]} {year}"
                    
                    logger.info(f"✓ Extracted date: {formatted}")
                    return (date_obj, formatted, gujarati)
                except ValueError:
                    pass
        
        logger.warning(f"Could not extract date from URL: {url}")
        return None
    
    def _parse_month(self, month_str: str) -> Optional[int]:
        """
        Parse month name to month number.
        
        Args:
            month_str: Month name (full or abbreviated)
            
        Returns:
            Month number (1-12) or None
        """
        month_str = month_str.lower()
        
        # Try full month name
        if month_str in self.MONTH_MAP:
            return self.MONTH_MAP[month_str]
        
        # Try abbreviated month name (first 3 letters)
        for full_name, month_num in self.MONTH_MAP.items():
            if full_name.startswith(month_str[:3]):
                return month_num
        
        return None
    
    def get_filename_date(self, url: str) -> str:
        """
        Get date string suitable for filename (YYYYMMDD format).
        
        Args:
            url: Quiz URL
            
        Returns:
            Date string in YYYYMMDD format, or current date if extraction fails
        """
        result = self.extract_date_from_url(url)
        if result:
            date_obj, _, _ = result
            return date_obj.strftime("%Y%m%d")
        
        # Fallback to current date
        return datetime.now().strftime("%Y%m%d")
