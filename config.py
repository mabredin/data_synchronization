import os
from typing import Optional

from dotenv import load_dotenv


load_dotenv()

FILE_NAME: Optional[str] = os.getenv('FILE_NAME')
COUNT_DAYS_FOR_SEARCH: Optional[str] = os.getenv('COUNT_DAYS_FOR_SEARCH')

# Database
DB_HOST: Optional[str] = os.getenv('DB_HOST')
DB_PORT: Optional[str] = os.getenv('DB_PORT')
DB_NAME: Optional[str] = os.getenv('DB_NAME')
DB_USER_NAME: Optional[str] = os.getenv('DB_USER_NAME')
DB_USER_PASSWORD: Optional[str] = os.getenv('DB_USER_PASSWORD')
