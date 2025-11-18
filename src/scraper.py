"""
Quiz scraping module for pendulumedu.com
Handles fetching quiz listings and individual quiz pages
"""

import time
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ScraperError(Exception):
    """Raised when scraping operations fail"""
    pass


class QuizScraper:
    """Scrapes quiz content from pendulumedu.com"""
    
    def __init__(self, session: requests.Session):
        """
        Initialize QuizScraper with authenticated session
        
        Args:
            session: Authenticated requests.Session object
        """
        self.session = session
        self.listing_url = "https://pendulumedu.com/quiz/current-affairs"
        
        # Configure retry strategy for network resilience
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def get_quiz_urls(self) -> List[str]:
        """
        Fetch and extract all quiz URLs from the listing page
        
        Returns:
            List of quiz URLs extracted from card-section divs
            
        Raises:
            ScraperError: If fetching or parsing fails
        """
        try:
            # Fetch the listing page
            response = self.session.get(
                self.listing_url,
                timeout=30,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all card-section divs
            card_sections = soup.find_all('div', class_='card-section')
            
            if not card_sections:
                print("Warning: No card-section divs found on listing page")
                return []
            
            # Extract URLs from anchor tags within card sections
            quiz_urls = []
            for card in card_sections:
                # Find anchor tag within the card
                anchor = card.find('a', href=True)
                if anchor:
                    url = anchor['href']
                    
                    # Convert relative URLs to absolute
                    if url.startswith('/'):
                        url = f"https://pendulumedu.com{url}"
                    elif not url.startswith('http'):
                        url = f"https://pendulumedu.com/{url}"
                    
                    quiz_urls.append(url)
            
            print(f"Found {len(quiz_urls)} quiz URLs on listing page")
            return quiz_urls
            
        except requests.exceptions.Timeout:
            raise ScraperError("Request timed out while fetching quiz listing")
        except requests.exceptions.HTTPError as e:
            raise ScraperError(f"HTTP error while fetching quiz listing: {e}")
        except requests.exceptions.RequestException as e:
            raise ScraperError(f"Network error while fetching quiz listing: {e}")
        except Exception as e:
            raise ScraperError(f"Unexpected error while fetching quiz URLs: {e}")
    
    def get_quiz_page(self, url: str) -> str:
        """
        Fetch individual quiz page HTML
        
        Args:
            url: URL of the quiz page to fetch
            
        Returns:
            HTML content as string
            
        Raises:
            ScraperError: If fetching fails
        """
        try:
            response = self.session.get(
                url,
                timeout=30,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            response.raise_for_status()
            
            return response.text
            
        except requests.exceptions.Timeout:
            raise ScraperError(f"Request timed out while fetching quiz page: {url}")
        except requests.exceptions.HTTPError as e:
            raise ScraperError(f"HTTP error while fetching quiz page: {e}")
        except requests.exceptions.RequestException as e:
            raise ScraperError(f"Network error while fetching quiz page: {e}")
        except Exception as e:
            raise ScraperError(f"Unexpected error while fetching quiz page: {e}")
    
    def submit_quiz(self, url: str) -> str:
        """
        Submit quiz to reveal solutions and return HTML with answers.
        
        The quiz requires JavaScript submission via the submit button.
        This method uses Selenium to:
        1. Load the quiz page
        2. Click the submit button
        3. Wait for solutions to appear
        4. Return the HTML with solutions
        
        Args:
            url: URL of the quiz page
            
        Returns:
            HTML content with solutions visible
            
        Raises:
            ScraperError: If submission fails
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from selenium.common.exceptions import TimeoutException, NoSuchElementException
            
            print(f"Using Selenium to submit quiz...")
            
            # Configure Chrome options for headless mode
            chrome_options = Options()
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            # Initialize the driver
            # Try with webdriver-manager first, fall back to system Chrome
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception as e:
                print(f"WebDriver Manager failed ({e}), trying system Chrome...")
                # Fall back to system Chrome (works if Chrome and ChromeDriver are in PATH)
                driver = webdriver.Chrome(options=chrome_options)
            
            try:
                # Load the quiz page
                print(f"Loading quiz page...")
                driver.get(url)
                
                # Transfer session cookies to Selenium
                for cookie in self.session.cookies:
                    cookie_dict = {
                        'name': cookie.name,
                        'value': cookie.value,
                        'domain': cookie.domain,
                        'path': cookie.path,
                    }
                    try:
                        driver.add_cookie(cookie_dict)
                    except Exception:
                        pass
                
                # Reload page with cookies
                driver.get(url)
                
                # Wait for page to load
                time.sleep(2)
                
                # Find and click the submit button
                print("Looking for submit button...")
                try:
                    # Try to find submit button by ID
                    submit_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "submit-ans"))
                    )
                    
                    # Scroll to button
                    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                    time.sleep(1)
                    
                    # Click the button
                    print("Clicking submit button...")
                    driver.execute_script("arguments[0].click();", submit_button)
                    
                    # Wait for solutions to appear
                    print("Waiting for solutions to load...")
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "solution-sec"))
                    )
                    
                    # Give it a moment to fully render
                    time.sleep(2)
                    
                    # Get the page source with solutions
                    html = driver.page_source
                    
                    # Verify solutions are present
                    soup = BeautifulSoup(html, 'html.parser')
                    solution_sections = soup.find_all('div', class_='solution-sec')
                    
                    if solution_sections:
                        print(f"✓ Solutions revealed! Found {len(solution_sections)} solution sections")
                        return html
                    else:
                        print("Warning: Submit clicked but no solutions found")
                        return html
                        
                except TimeoutException:
                    print("Warning: Submit button not found or timeout waiting for solutions")
                    # Return current page HTML anyway
                    return driver.page_source
                    
            finally:
                # Always close the driver
                driver.quit()
                
        except ImportError:
            raise ScraperError(
                "Selenium is required for quiz submission. Install with: pip install selenium"
            )
        except Exception as e:
            raise ScraperError(f"Error during Selenium quiz submission: {str(e)}")
    

