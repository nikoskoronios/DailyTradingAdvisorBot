from TradingPack.Database.connection import conn
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


"""cursor = conn.cursor()
cursor.execute("SELECT * FROM Sector")
Sectors  = cursor.fetchall()
print(Sectors)
cursor.execute("SELECT * FROM Industry")
Industries = cursor.fetchall()
print(Industries)"""

url="https://finance.yahoo.com/sectors/technology/"

CHROMEDRIVER_PATH = r"C:\Users\User\Desktop\DailyTradingAdvisorBot\chromedriver-win64\chromedriver.exe"
options = Options()
#options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

try:
    # ➤ Αν ο χρήστης ανακατευθυνθεί στο consent.yahoo.com
    if "consent.yahoo.com" in driver.current_url:
        print("⚠️ Εντοπίστηκε consent page")

        # ➤ Κάνε click στο κουμπί με class="accept-all"
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "accept-all"))
        )
        accept_button.click()
        print("✅ Έγινε click στο 'Αποδοχή όλων'")

        # ➤ Δώσε χρόνο να γίνει redirect στο finance.yahoo.com
        time.sleep(5)

except Exception as e:
    print("⚠️ Πρόβλημα με το κουμπί αποδοχής:", e)

# ➤ Δώσε χρόνο για να φορτωθεί η τελική σελίδα
time.sleep(7)

# ➤ Αποθήκευση HTML
with open("dump.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

driver.quit()
print("✅ Τέλος – αποθηκεύτηκε dump.html")