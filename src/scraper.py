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
        Submit quiz to reveal solutions using POST request method.
        
        The website works as follows:
        1. Initial page has placeholder answers ("Option D")
        2. POST to /quiz/quizanwers with quiz ID updates server session
        3. GET the quiz page again - response contains actual answers
        
        Args:
            url: URL of the quiz page
            
        Returns:
            HTML content with solutions visible
            
        Raises:
            ScraperError: If submission fails
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info("=" * 80)
        logger.info("SUBMIT_QUIZ: Starting quiz submission")
        logger.info(f"SUBMIT_QUIZ: URL = {url}")
        logger.info("=" * 80)
        
        try:
            # Method 1: POST request (fast and reliable)
            logger.info("SUBMIT_QUIZ: Trying POST request method...")
            html = self._submit_quiz_post(url)
            
            # Verify we got correct answers
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            solution_sections = soup.find_all('div', class_='solution-sec')
            
            if solution_sections:
                first_head = solution_sections[0].find('div', class_='head')
                if first_head:
                    head_text = first_head.get_text(strip=True)
                    logger.info(f"SUBMIT_QUIZ: First head div: '{head_text}'")
                    
                    if 'Correct Answer:' in head_text or 'सही उत्तर:' in head_text:
                        logger.info("SUBMIT_QUIZ: ✓ POST method successful!")
                        return html
            
            logger.warning("SUBMIT_QUIZ: POST method didn't work, trying Selenium...")
            return self._submit_quiz_selenium(url)
            
        except Exception as e:
            logger.error(f"SUBMIT_QUIZ: POST method failed: {e}")
            logger.info("SUBMIT_QUIZ: Falling back to Selenium...")
            return self._submit_quiz_selenium(url)
    
    def _submit_quiz_post(self, url: str) -> str:
        """
        Submit quiz using POST request and return updated HTML.
        
        Args:
            url: URL of the quiz page
            
        Returns:
            HTML with solutions
        """
        import logging
        logger = logging.getLogger(__name__)
        from bs4 import BeautifulSoup
        
        logger.info("POST: Fetching initial page to get quiz ID...")
        initial_html = self.get_quiz_page(url)
        
        soup = BeautifulSoup(initial_html, 'html.parser')
        quiz_id_input = soup.find('input', {'id': 'intQuizId'})
        english_quiz_id_input = soup.find('input', {'id': 'intEnglishQuizId'})
        
        if not quiz_id_input or not english_quiz_id_input:
            raise ScraperError("Could not find quiz ID inputs in HTML")
        
        quiz_id = quiz_id_input.get('value')
        english_quiz_id = english_quiz_id_input.get('value')
        
        logger.info(f"POST: Quiz ID = {quiz_id}, English Quiz ID = {english_quiz_id}")
        
        # Make POST request to submit quiz
        logger.info("POST: Submitting quiz...")
        submit_url = "https://pendulumedu.com/quiz/quizanwers"
        
        form_data = {
            'intQuizId': quiz_id,
            'intEnglishQuizId': english_quiz_id,
            'txtCurrentURL': url,
            'txtCurrentTime': '0',
            'txtLoginPopupStatus': 'no',
            'pauseBtnhms': 'resume'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://pendulumedu.com',
            'Referer': url,
        }
        
        response = self.session.post(
            submit_url,
            data=form_data,
            headers=headers,
            timeout=30,
            allow_redirects=True
        )
        
        logger.info(f"POST: Response status = {response.status_code}")
        logger.info(f"POST: Final URL = {response.url}")
        
        # The POST updates the session. Now GET the quiz page again.
        logger.info("POST: Fetching quiz page again (should have answers now)...")
        time.sleep(2)  # Give server a moment
        
        updated_html = self.get_quiz_page(url)
        
        # Save for debugging
        try:
            with open('debug_scraped_quiz.html', 'w', encoding='utf-8') as f:
                f.write(updated_html)
            logger.info("POST: Saved HTML to debug_scraped_quiz.html")
        except Exception:
            pass
        
        return updated_html
    
    def _submit_quiz_selenium(self, url: str) -> str:
        """
        Use Selenium to click submit button and wait for answers to load.
        
        Args:
            url: URL of the quiz page
            
        Returns:
            HTML content with solutions visible
            
        Raises:
            ScraperError: If submission fails
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info("=" * 80)
        logger.info("SELENIUM: Method started")
        logger.info(f"SELENIUM: URL = {url}")
        logger.info("=" * 80)
        
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from selenium.common.exceptions import TimeoutException, NoSuchElementException
            
            logger.info("SELENIUM: Imports successful")
            
            logger.info("SELENIUM: Configuring Chrome options...")
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
            
            logger.info("SELENIUM: Initializing Chrome driver...")
            # Initialize the driver
            # Try with webdriver-manager first, fall back to system Chrome
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("SELENIUM: ✓ Chrome driver initialized with webdriver-manager")
            except Exception as e:
                logger.warning(f"SELENIUM: WebDriver Manager failed ({e}), trying system Chrome...")
                # Fall back to system Chrome (works if Chrome and ChromeDriver are in PATH)
                driver = webdriver.Chrome(options=chrome_options)
                logger.info("SELENIUM: ✓ Chrome driver initialized with system Chrome")
            
            # Execute stealth scripts to avoid detection
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
            })
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            try:
                # Load the quiz page
                logger.info(f"SELENIUM: Loading quiz page: {url}")
                driver.get(url)
                logger.info("SELENIUM: ✓ Page loaded")
                
                # Add random delay to appear more human-like
                wait_time = 2 + (time.time() % 2)
                logger.info(f"SELENIUM: Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                
                # Transfer session cookies to Selenium
                logger.info("SELENIUM: Transferring session cookies...")
                cookie_count = 0
                for cookie in self.session.cookies:
                    cookie_dict = {
                        'name': cookie.name,
                        'value': cookie.value,
                        'domain': cookie.domain,
                        'path': cookie.path,
                    }
                    try:
                        driver.add_cookie(cookie_dict)
                        cookie_count += 1
                    except Exception:
                        pass
                logger.info(f"SELENIUM: ✓ Transferred {cookie_count} cookies")
                
                # Reload page with cookies
                logger.info("SELENIUM: Reloading page with cookies...")
                driver.get(url)
                logger.info("SELENIUM: ✓ Page reloaded with authentication")
                
                # Wait for page to load
                logger.info("SELENIUM: Waiting 2 seconds for page to fully load...")
                time.sleep(2)
                
                # Find and click the submit button
                logger.info("SELENIUM: Looking for submit button (ID: submit-ans)...")
                try:
                    # Try to find submit button by ID
                    logger.info("SELENIUM: Waiting for submit button to appear...")
                    submit_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "submit-ans"))
                    )
                    logger.info("SELENIUM: ✓ Submit button found!")
                    
                    # Scroll to button
                    logger.info("SELENIUM: Scrolling to submit button...")
                    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                    time.sleep(1)
                    
                    # Click the button
                    logger.info("SELENIUM: *** CLICKING SUBMIT BUTTON NOW ***")
                    driver.execute_script("arguments[0].click();", submit_button)
                    logger.info("SELENIUM: ✓ Submit button clicked!")
                    
                    # Wait for solutions to appear
                    logger.info("SELENIUM: Waiting for solution-sec divs to appear...")
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "solution-sec"))
                    )
                    logger.info("SELENIUM: ✓ solution-sec divs found")
                    
                    # CRITICAL: Wait for the head div text to change from "Solution:" to "Correct Answer:"
                    logger.info("SELENIUM: Waiting for head div to update (30 seconds timeout)...")
                    try:
                        WebDriverWait(driver, 30).until(
                            lambda d: any(
                                "Correct Answer:" in head.text or "सही उत्तर:" in head.text
                                for head in d.find_elements(By.CSS_SELECTOR, ".solution-sec .head")
                                if head.text.strip() and head.text.strip() != "Solution:"
                            )
                        )
                        logger.info("SELENIUM: ✓ Head div updated with 'Correct Answer:' text!")
                    except TimeoutException:
                        logger.error("SELENIUM: ✗ TIMEOUT - Head div never updated!")
                        # Check what we have
                        heads = driver.find_elements(By.CSS_SELECTOR, ".solution-sec .head")
                        if heads:
                            logger.error(f"SELENIUM: Found {len(heads)} head divs")
                            for i, head in enumerate(heads[:3]):
                                logger.error(f"SELENIUM: Head {i+1}: '{head.text[:100]}'")
                        
                        # Try waiting longer
                        logger.info("SELENIUM: Waiting additional 10 seconds...")
                        time.sleep(10)
                        
                        # Check again
                        heads = driver.find_elements(By.CSS_SELECTOR, ".solution-sec .head")
                        if heads and heads[0].text.strip():
                            logger.info(f"SELENIUM: After extra wait, head div: '{heads[0].text[:100]}'")
                    
                    # Wait for ans-text div to have content
                    logger.info("SELENIUM: Waiting for explanation content...")
                    try:
                        WebDriverWait(driver, 20).until(
                            lambda d: any(
                                len(ans_text.find_elements(By.TAG_NAME, "li")) > 0 or
                                len(ans_text.find_elements(By.TAG_NAME, "p")) > 0
                                for ans_text in d.find_elements(By.CLASS_NAME, "ans-text")
                            )
                        )
                        logger.info("SELENIUM: ✓ Explanation content detected")
                    except TimeoutException:
                        logger.warning("SELENIUM: Timeout waiting for explanation content")
                    
                    # Give it final time to render
                    logger.info("SELENIUM: Final 5 second wait for complete render...")
                    time.sleep(5)
                    
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
    

