
import os
from dotenv import load_dotenv

load_dotenv()

TMP_OUTPUT_PATH = os.getenv("TMP_OUTPUT_PATH", "./temp")
FILE_OUTPUT_PATH = os.getenv("FILE_OUTPUT_PATH", "./output")
REQUEST_PER_SECOND = int(os.getenv("REQUEST_PER_SECOND", "3"))
DIR_NAME = os.getenv("DIR_NAME")
KEY = os.getenv("KEY")
