# Requirements Document

## Introduction

This document specifies the requirements for an automated web scraping system that extracts Current Affairs Quiz content from pendulumedu.com, translates it to Gujarati, generates branded PDF documents, and distributes them via Telegram. The system operates on a daily schedule using GitHub Actions to provide timely educational content to subscribers.

## Glossary

- **Scraper System**: The complete automated solution that performs login, scraping, translation, PDF generation, and Telegram distribution
- **Quiz Page**: A web page on pendulumedu.com containing a Current Affairs quiz with questions, options, and solutions
- **Quiz Card**: An HTML element on the listing page that contains a link to an individual quiz
- **Solution Reveal**: The process of submitting a quiz to make answers and explanations visible
- **Translation Service**: The component that converts English text to Gujarati using an API or LLM
- **PDF Generator**: The component that creates formatted PDF documents with branding
- **Telegram Bot**: The automated service that sends PDF files to a Telegram channel
- **Tracking File**: A JSON file (scraped_urls.json) that maintains a list of processed quiz URLs
- **GitHub Actions Workflow**: The automated CI/CD pipeline that executes the scraper on a schedule

## Requirements

### Requirement 1

**User Story:** As a content distributor, I want the system to authenticate with pendulumedu.com, so that I can access protected quiz content

#### Acceptance Criteria

1. WHEN the Scraper System initiates, THE Scraper System SHALL submit credentials to https://pendulumedu.com/login using the emailId and password fields
2. THE Scraper System SHALL maintain session cookies after successful authentication
3. IF authentication fails, THEN THE Scraper System SHALL log the error and terminate execution
4. THE Scraper System SHALL retrieve credentials from environment variables or GitHub Secrets

### Requirement 2

**User Story:** As a content distributor, I want the system to identify new quizzes, so that I avoid processing duplicate content

#### Acceptance Criteria

1. THE Scraper System SHALL fetch the quiz listing page at https://pendulumedu.com/quiz/current-affairs
2. THE Scraper System SHALL extract all quiz URLs from anchor tags within div elements matching class "card-section"
3. THE Scraper System SHALL compare extracted URLs against entries in the Tracking File
4. WHEN a quiz URL is not present in the Tracking File, THE Scraper System SHALL mark it as new
5. THE Scraper System SHALL process only quiz URLs marked as new

### Requirement 3

**User Story:** As a content distributor, I want the system to reveal quiz solutions, so that I can extract complete question and answer data

#### Acceptance Criteria

1. WHEN the Scraper System accesses a Quiz Page, THE Scraper System SHALL locate the submit button with id "submit-ans"
2. THE Scraper System SHALL trigger the submit action to reveal solutions
3. THE Scraper System SHALL wait for the page to update with solution content before extraction
4. THE Scraper System SHALL verify that solution sections are visible after submission

### Requirement 4

**User Story:** As a content distributor, I want the system to extract structured quiz data, so that I can process and format it for distribution

#### Acceptance Criteria

1. THE Scraper System SHALL extract question text from div elements with class "q-name"
2. THE Scraper System SHALL extract all option texts from li elements containing class "containerr-text-opt"
3. THE Scraper System SHALL preserve option labels (A, B, C, D) with their corresponding text
4. THE Scraper System SHALL extract the correct answer from div elements with class "solution-sec"
5. THE Scraper System SHALL extract explanation text from div elements with class "ans-text"
6. THE Scraper System SHALL maintain the association between questions, options, answers, and explanations

### Requirement 5

**User Story:** As a content distributor serving Gujarati-speaking audiences, I want all quiz content translated to Gujarati, so that users can understand the material in their preferred language

#### Acceptance Criteria

1. THE Translation Service SHALL translate question text from English to Gujarati
2. THE Translation Service SHALL translate all option texts from English to Gujarati
3. THE Translation Service SHALL translate correct answer descriptions from English to Gujarati
4. THE Translation Service SHALL translate explanation text from English to Gujarati
5. THE Translation Service SHALL preserve option labels (A, B, C, D) without translation
6. THE Translation Service SHALL preserve the channel name "CurrentAdda" without translation
7. THE Translation Service SHALL preserve the channel link without translation

### Requirement 6

**User Story:** As a content distributor, I want professionally formatted PDF documents with branding, so that I can maintain brand identity and provide quality content

#### Acceptance Criteria

1. THE PDF Generator SHALL create a cover page containing the channel name "CurrentAdda"
2. THE PDF Generator SHALL include the channel link "https://t.me/currentadda" on the cover page
3. THE PDF Generator SHALL display the text "Providing Current Affairs since 2019" on the cover page
4. THE PDF Generator SHALL display the current date in IST timezone on the cover page
5. THE PDF Generator SHALL display the total number of questions on the cover page
6. THE PDF Generator SHALL render Gujarati text using Unicode-compatible fonts
7. THE PDF Generator SHALL format each question in a container box with question number, options, correct answer, and explanation
8. THE PDF Generator SHALL highlight the correct answer in green color
9. THE PDF Generator SHALL apply bold formatting to question text
10. THE PDF Generator SHALL maintain consistent spacing and borders throughout the document

### Requirement 7

**User Story:** As a content distributor, I want PDF files automatically sent to my Telegram channel, so that subscribers receive content without manual intervention

#### Acceptance Criteria

1. THE Telegram Bot SHALL authenticate using a bot token from environment variables
2. THE Telegram Bot SHALL send the generated PDF file to the channel "@currentadda"
3. THE Telegram Bot SHALL include a caption with the text "Today's Current Affairs Quiz PDF", source attribution, and channel link
4. IF the Telegram send operation fails, THEN THE Telegram Bot SHALL log the error with details

### Requirement 8

**User Story:** As a content distributor, I want the system to run automatically every day at 9:00 AM IST, so that content is delivered consistently without manual execution

#### Acceptance Criteria

1. THE GitHub Actions Workflow SHALL execute daily at 9:00 AM IST (3:00 AM UTC)
2. THE GitHub Actions Workflow SHALL install required Python dependencies before execution
3. THE GitHub Actions Workflow SHALL execute the scraping, translation, PDF generation, and Telegram distribution sequence
4. THE GitHub Actions Workflow SHALL commit the updated Tracking File to the repository after successful execution
5. IF any step in the workflow fails, THEN THE GitHub Actions Workflow SHALL log the error and terminate

### Requirement 9

**User Story:** As a content distributor, I want the system to track processed quizzes, so that I maintain a historical record and prevent reprocessing

#### Acceptance Criteria

1. THE Scraper System SHALL read the Tracking File at data/scraped_urls.json before processing
2. WHEN a quiz is successfully processed, THE Scraper System SHALL append its URL to the Tracking File
3. THE Scraper System SHALL persist the updated Tracking File to disk after each successful quiz processing
4. IF the Tracking File does not exist, THEN THE Scraper System SHALL create it with an empty list

### Requirement 10

**User Story:** As a system administrator, I want sensitive credentials stored securely, so that authentication information is not exposed in the codebase

#### Acceptance Criteria

1. THE Scraper System SHALL retrieve login email from a GitHub Secret named LOGIN_EMAIL
2. THE Scraper System SHALL retrieve login password from a GitHub Secret named LOGIN_PASSWORD
3. THE Telegram Bot SHALL retrieve the bot token from a GitHub Secret named TELEGRAM_BOT_TOKEN
4. THE Scraper System SHALL NOT contain hardcoded credentials in any source file
