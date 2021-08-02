import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
FB_ACCOUNT = os.getenv("FB_ACCOUNT")  # 通常固定不變之參數以全大寫命名
FB_PASSWORD = os.getenv("FB_PASSWORD")

CHROMEDRIVER_DIR = "chromedriver"
CHROMEDRIVER_EXE_DIR = os.path.join(CHROMEDRIVER_DIR, "chromedriver.exe")
OUTPUTS_DIR = "outputs"
