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
            # Add realistic browser headers to avoid detection
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
            }
            
            # Add small delay to appear more human-like
            time.sleep(1)
            
            # Fetch the listing page
            response = self.session.get(
                self.listing_url,
                timeout=30,
                headers=headers
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
            # Add realistic browser headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Referer': 'https://pendulumedu.com/quiz/current-affairs',
            }
            
            # Add small delay
            time.sleep(1)
            
            response = self.session.get(
                url,
                timeout=30,
                headers=headers
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
        
        The quiz page loads with placeholder answers (all showing "Option D").
        When the submit button is clicked, it makes a POST request to /quiz/quizanwers
        which returns the actual answers, and JavaScript updates the page.
        
        This method:
        1. Loads the quiz page to get the quiz ID
        2. Makes a POST request to /quiz/quizanwers to trigger answer reveal
        3. Reloads the page to get the updated HTML with correct answers
        
        Args:
            url: URL of the quiz page
            
        Returns:
            HTML content with solutions visible
            
        Raises:
            ScraperError: If submission fails
        """
        # POST request doesn't work - the server stores submission in session
        # but doesn't update the HTML. JavaScript is required to fetch and display answers.
        # Use Selenium directly.
        print("Using Selenium to submit quiz (POST method doesn't work)...")
        return self._submit_quiz_selenium(url)
    
    def _submit_quiz_selenium(self, url: str) -> str:
        """
        Fallback method using Selenium to submit quiz.
        
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
            
            # Configure Chrome options for headless mode with anti-detection
            chrome_options = Options()
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Add preferences to appear more like a real browser
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0,
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
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
            
            # Execute stealth scripts to avoid detection
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
            })
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            try:
                # Load the quiz page
                print(f"Loading quiz page...")
                driver.get(url)
                
                # Add random delay to appear more human-like
                time.sleep(2 + (time.time() % 2))  # 2-4 seconds
                
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
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "solution-sec"))
                    )
                    
                    # CRITICAL: Wait for the solution-sec divs to have display:block (not display:none)
                    print("Waiting for solution-sec to become visible...")
                    try:
                        WebDriverWait(driver, 15).until(
                            lambda d: any(
                                sol.value_of_css_property("display") == "block"
                                for sol in d.find_elements(By.CLASS_NAME, "solution-sec")
                            )
                        )
                        print("✓ solution-sec divs are now visible")
                    except TimeoutException:
                        print("⚠️ Warning: solution-sec divs still hidden, trying to proceed...")
                    
                    # Wait specifically for the head div to contain "Correct Answer" text
                    print("Waiting for correct answer to appear in head div...")
                    try:
                        WebDriverWait(driver, 15).until(
                            lambda d: any(
                                "Correct Answer:" in head.text
                                for head in d.find_elements(By.CSS_SELECTOR, ".solution-sec .head")
                                if head.text.strip()
                            )
                        )
                        print("✓ 'Correct Answer:' text detected in head divs")
                    except TimeoutException:
                        print("⚠️ Warning: Timeout waiting for 'Correct Answer:' text...")
                        # Try to check what we actually have
                        heads = driver.find_elements(By.CSS_SELECTOR, ".solution-sec .head")
                        if heads:
                            print(f"  Found {len(heads)} head divs, first one says: '{heads[0].text[:50]}'")
                    
                    # Wait for ans-text div to have list items or paragraphs
                    print("Waiting for explanation content to load...")
                    try:
                        WebDriverWait(driver, 15).until(
                            lambda d: any(
                                len(ans_text.find_elements(By.TAG_NAME, "li")) > 0 or
                                len(ans_text.find_elements(By.TAG_NAME, "p")) > 0
                                for ans_text in d.find_elements(By.CLASS_NAME, "ans-text")
                            )
                        )
                        print("✓ Explanation content (li/p tags) detected")
                    except TimeoutException:
                        print("⚠️ Warning: Timeout waiting for explanation content...")
                    
                    # Give it extra time to fully render all content
                    print("Waiting for final render...")
                    time.sleep(3)
                    
                    # Get the page source with solutions
                    html = driver.page_source
                    
                    # Verify solutions are present and have content
                    soup = BeautifulSoup(html, 'html.parser')
                    solution_sections = soup.find_all('div', class_='solution-sec')
                    
                    if solution_sections:
                        print(f"✓ Solutions revealed! Found {len(solution_sections)} solution sections")
                        
                        # Debug: Check first solution section
                        first_solution = solution_sections[0]
                        head_div = first_solution.find('div', class_='head')
                        ans_text_div = first_solution.find('div', class_='ans-text')
                        
                        if head_div:
                            print(f"  First head div: '{head_div.get_text(strip=True)[:80]}'")
                        if ans_text_div:
                            ans_text_content = ans_text_div.get_text(strip=True)
                            print(f"  First ans-text length: {len(ans_text_content)} chars")
                            if len(ans_text_content) > 0:
                                print(f"  First ans-text preview: '{ans_text_content[:80]}'")
                        
                        # Save HTML for debugging
                        try:
                            with open('debug_scraped_quiz.html', 'w', encoding='utf-8') as f:
                                f.write(html)
                            print("  Debug: Saved scraped HTML to debug_scraped_quiz.html")
                        except Exception as e:
                            print(f"  Warning: Could not save debug HTML: {e}")
                        
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
    

