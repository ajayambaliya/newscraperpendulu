"""
Quiz scraping module for pendulumedu.com
Handles fetching quiz listings and individual quiz pages
"""

import os
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Try to import Playwright at module level
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    sync_playwright = None


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
        Submit quiz to reveal solutions using Playwright.
        
        Playwright handles JavaScript execution properly, unlike Selenium in headless mode.
        
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
        logger.info("SUBMIT_QUIZ: Starting quiz submission with Playwright")
        logger.info(f"SUBMIT_QUIZ: URL = {url}")
        logger.info("=" * 80)
        
        return self._submit_quiz_playwright(url)
    
    def _submit_quiz_playwright(self, url: str) -> str:
        """
        Submit quiz using Playwright (better JavaScript support than Selenium).
        
        Args:
            url: URL of the quiz page
            
        Returns:
            HTML with solutions
        """
        import logging
        logger = logging.getLogger(__name__)
        
        if not PLAYWRIGHT_AVAILABLE:
            raise ScraperError("Playwright not installed. Run: pip install playwright && playwright install chromium")
        
        logger.info("PLAYWRIGHT: Starting browser...")
        
        with sync_playwright() as p:
            # Launch browser (headless by default, can be changed for debugging)
            use_headless = os.getenv('USE_HEADLESS', 'true').lower() == 'true'
            browser = p.chromium.launch(headless=use_headless)
            
            logger.info(f"PLAYWRIGHT: Browser launched (headless={use_headless})")
            
            # Create context and page
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            try:
                # Get credentials
                email = os.getenv('LOGIN_EMAIL')
                password = os.getenv('LOGIN_PASSWORD')
                
                if not email or not password:
                    raise ScraperError("LOGIN_EMAIL and LOGIN_PASSWORD must be set")
                
                # First, login to the website
                logger.info("PLAYWRIGHT: Logging in...")
                login_url = "https://pendulumedu.com/login"
                page.goto(login_url, wait_until='networkidle', timeout=30000)
                logger.info("PLAYWRIGHT: ✓ Login page loaded")
                
                # Fill login form
                logger.info("PLAYWRIGHT: Filling login credentials...")
                page.fill('input[name="emailId"]', email)
                page.fill('input[name="password"]', password)
                
                # Click submit button
                logger.info("PLAYWRIGHT: Submitting login form...")
                page.click('button[type="submit"]')
                
                # Wait for login to complete (page will redirect)
                logger.info("PLAYWRIGHT: Waiting for login to complete...")
                page.wait_for_load_state('networkidle', timeout=10000)
                logger.info(f"PLAYWRIGHT: ✓ Logged in, current URL: {page.url}")
                
                # Now navigate to quiz page
                logger.info(f"PLAYWRIGHT: Loading quiz page: {url}")
                page.goto(url, wait_until='networkidle', timeout=30000)
                logger.info(f"PLAYWRIGHT: ✓ Quiz page loaded, URL: {page.url}")
                
                # Save screenshot for debugging
                try:
                    page.screenshot(path='debug_playwright_page.png')
                    logger.info("PLAYWRIGHT: Saved screenshot to debug_playwright_page.png")
                except Exception:
                    pass
                
                # Check if quiz already has answers (already submitted before)
                logger.info("PLAYWRIGHT: Checking if quiz already has answers...")
                try:
                    first_head = page.locator('.solution-sec .head').first
                    head_text = first_head.text_content(timeout=2000)
                    logger.info(f"PLAYWRIGHT: Head div text: '{head_text}'")
                    
                    if 'Correct Answer:' in head_text or 'सही उत्तर:' in head_text:
                        logger.info("PLAYWRIGHT: ✅ Quiz already submitted! Answers are visible.")
                        # No need to click submit, answers are already there
                    else:
                        logger.info("PLAYWRIGHT: Quiz not submitted yet, need to click submit button")
                        raise Exception("Need to submit")
                        
                except Exception:
                    # Quiz not submitted yet, need to click submit button
                    logger.info("PLAYWRIGHT: Looking for submit button...")
                    try:
                        submit_button = page.locator('#submit-ans')
                        submit_button.wait_for(state='visible', timeout=10000)
                        logger.info("PLAYWRIGHT: ✓ Submit button found")
                        
                        # Scroll to button
                        submit_button.scroll_into_view_if_needed()
                        page.wait_for_timeout(1000)
                        
                        # Set up dialog handler BEFORE clicking
                        def handle_dialog(dialog):
                            logger.info(f"PLAYWRIGHT: Alert: '{dialog.message}'")
                            dialog.accept()
                        
                        page.on('dialog', handle_dialog)
                        
                        # Click submit
                        logger.info("PLAYWRIGHT: *** CLICKING SUBMIT BUTTON ***")
                        submit_button.click()
                        logger.info("PLAYWRIGHT: ✓ Submit button clicked")
                        
                        # Wait for solutions to update
                        logger.info("PLAYWRIGHT: Waiting for solutions to load...")
                        
                        # Wait a moment for JavaScript to execute
                        page.wait_for_timeout(2000)
                        
                        # Check if solutions loaded by looking at the head div text
                        max_attempts = 15  # 15 seconds total
                        for attempt in range(max_attempts):
                            try:
                                head_text = page.locator('.solution-sec .head').first.text_content()
                                logger.info(f"PLAYWRIGHT: Attempt {attempt + 1}: Head div = '{head_text}'")
                                
                                if 'Correct Answer:' in head_text or 'सही उत्तर:' in head_text:
                                    logger.info("PLAYWRIGHT: ✓ Solutions loaded!")
                                    break
                            except Exception:
                                pass
                            
                            page.wait_for_timeout(1000)
                        else:
                            logger.warning("PLAYWRIGHT: Timeout waiting for solutions, continuing anyway...")
                        
                        # Wait a bit more for complete render
                        page.wait_for_timeout(2000)
                        
                    except Exception as e:
                        logger.error(f"PLAYWRIGHT: Submit button not found: {e}")
                        logger.error(f"PLAYWRIGHT: Current URL: {page.url}")
                        raise
                
                # Get HTML
                html = page.content()
                
                # Save for debugging
                try:
                    with open('debug_scraped_quiz.html', 'w', encoding='utf-8') as f:
                        f.write(html)
                    logger.info("PLAYWRIGHT: Saved HTML to debug_scraped_quiz.html")
                except Exception:
                    pass
                
                # Verify we got correct answers
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                solution_sections = soup.find_all('div', class_='solution-sec')
                
                if solution_sections:
                    first_head = solution_sections[0].find('div', class_='head')
                    if first_head:
                        head_text = first_head.get_text(strip=True)
                        logger.info(f"PLAYWRIGHT: First head div: '{head_text}'")
                        
                        if 'Correct Answer:' in head_text or 'सही उत्तर:' in head_text:
                            logger.info("PLAYWRIGHT: ✅ SUCCESS! Got correct answers!")
                            return html
                        else:
                            logger.error(f"PLAYWRIGHT: ✗ FAILED - Head shows '{head_text}'")
                
                logger.warning("PLAYWRIGHT: Returning HTML anyway...")
                return html
                
            finally:
                browser.close()
                logger.info("PLAYWRIGHT: Browser closed")
    
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
        
        # Extract all form inputs to include answer selections
        logger.info("POST: Extracting form data...")
        form = soup.find('form', {'id': 'pendu_quiz'})
        form_data = {
            'intQuizId': quiz_id,
            'intEnglishQuizId': english_quiz_id,
            'txtCurrentURL': url,
            'txtCurrentTime': '0',
            'txtLoginPopupStatus': 'no',
            'pauseBtnhms': 'resume'
        }
        
        # Add all answer options (select first option for each question)
        if form:
            inputs = form.find_all('input', {'type': 'radio'})
            logger.info(f"POST: Found {len(inputs)} radio inputs")
            
            # Group by question and select first option for each
            questions_seen = set()
            for inp in inputs:
                name = inp.get('name')
                value = inp.get('value')
                if name and value and name not in questions_seen:
                    form_data[name] = value
                    questions_seen.add(name)
            
            logger.info(f"POST: Selected answers for {len(questions_seen)} questions")
        
        # Make POST request to submit quiz
        logger.info("POST: Submitting quiz with answers...")
        submit_url = "https://pendulumedu.com/quiz/quizanwers"
        
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
            # Configure Chrome options - try without headless first
            chrome_options = Options()
            
            # Only use headless if environment variable is set
            use_headless = os.getenv('USE_HEADLESS', 'true').lower() == 'true'
            if use_headless:
                logger.info("SELENIUM: Using headless mode")
                chrome_options.add_argument('--headless=new')
            else:
                logger.info("SELENIUM: Using visible browser mode")
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Enable JavaScript
            chrome_options.add_argument('--enable-javascript')
            
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
                
                # Wait for page to load
                time.sleep(3)
                
                # Check if we need to login (look for login elements)
                try:
                    # Check if there's a login/signup button in header
                    signin_button = driver.find_element(By.CSS_SELECTOR, ".signin-btn, .signup-btn")
                    logger.info("SELENIUM: Not logged in, need to login...")
                    
                    # Get credentials
                    email = os.getenv('LOGIN_EMAIL')
                    password = os.getenv('LOGIN_PASSWORD')
                    
                    if not email or not password:
                        raise ScraperError("LOGIN_EMAIL and LOGIN_PASSWORD must be set")
                    
                    # Click signin button to open login modal/page
                    logger.info("SELENIUM: Clicking signin button...")
                    driver.execute_script("arguments[0].click();", signin_button)
                    time.sleep(2)
                    
                    # Fill login form (might be in modal or redirected page)
                    logger.info("SELENIUM: Looking for login form...")
                    email_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "emailId"))
                    )
                    password_input = driver.find_element(By.ID, "password")
                    
                    logger.info("SELENIUM: Filling login credentials...")
                    email_input.clear()
                    email_input.send_keys(email)
                    password_input.clear()
                    password_input.send_keys(password)
                    
                    # Click login button
                    login_button = driver.find_element(By.CSS_SELECTOR, "button[onclick*='sign_in']")
                    logger.info("SELENIUM: Clicking login button...")
                    driver.execute_script("arguments[0].click();", login_button)
                    
                    # Wait for login
                    time.sleep(3)
                    
                    # Navigate back to quiz if we were redirected
                    if driver.current_url != url:
                        logger.info(f"SELENIUM: Navigating back to quiz: {url}")
                        driver.get(url)
                        time.sleep(2)
                    
                    logger.info("SELENIUM: ✓ Logged in successfully")
                    
                except Exception as e:
                    logger.info(f"SELENIUM: Already logged in or login not needed: {e}")
                
                logger.info("SELENIUM: ✓ Quiz page ready")
                
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
                    
                    # Wait a moment for any alerts or modals
                    time.sleep(2)
                    
                    # Check for "already attempted" alert
                    try:
                        logger.info("SELENIUM: Checking for alerts...")
                        alert = driver.switch_to.alert
                        alert_text = alert.text
                        logger.info(f"SELENIUM: Alert found: '{alert_text}'")
                        
                        if "already attempted" in alert_text.lower():
                            logger.info("SELENIUM: Quiz already attempted - accepting alert...")
                            alert.accept()
                            logger.info("SELENIUM: ✓ Alert accepted")
                            time.sleep(2)  # Wait for page to update after alert
                    except Exception:
                        logger.info("SELENIUM: No alert found (this is normal)")
                    
                    # Check for login modal
                    try:
                        login_modal = driver.find_element(By.ID, "myModal-score-card")
                        if login_modal.is_displayed():
                            logger.error("SELENIUM: ✗ Login modal appeared - cookies not working!")
                            # Try to close modal and proceed anyway
                            close_button = driver.find_element(By.CSS_SELECTOR, "#myModal-score-card .close")
                            close_button.click()
                            time.sleep(1)
                    except Exception:
                        logger.info("SELENIUM: No login modal (good!)")
                    
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
    

