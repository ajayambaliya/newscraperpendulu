# Beautiful PDF Generator
import os
import logging
from pathlib import Path
from datetime import datetime
import pytz

from .parser import QuizQuestion
from .translator import TranslatedQuizData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self, output_dir='pdfs'):
        self.output_dir = output_dir
        self.html_output_dir = 'output'
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.html_output_dir).mkdir(parents=True, exist_ok=True)
        self.channel_name = 'CurrentAdda'
        self.channel_link = 't.me/currentadda'
        logger.info('PDF Generator initialized')
