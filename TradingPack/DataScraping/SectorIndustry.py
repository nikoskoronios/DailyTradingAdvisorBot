from TradingPack.Database.connection import conn
from TradingPack.DataTransformation.SectorIndustry import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from datetime import datetime


def ScrapingSectorIndustry (type, id, name, url):

    CHROMEDRIVER_PATH = r"C:\Users\User\Desktop\DailyTradingAdvisorBot\chromedriver-win64\chromedriver.exe"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    # Accept Cookies page
    try:
        if "consent.yahoo.com" in driver.current_url:
            print("⚠️ Consent page")

            accept_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "accept-all")))
            accept_button.click()
            print("✅ Accept All")

            time.sleep(1)

    except Exception as e:
        print("⚠️ Error in Accepting proccess:", e)

    # Wait until the page loaded
    time.sleep(1)

    # We took the html
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Collect the returns
    # Find performance cards
    cards = soup.find_all("section", {"class": "card small yf-ispmdb bdr sticky noBackGround"})
    returns = {}
    for card in cards:
        try:
            title_tag = card.find("h3", {"class": "title font-condensed yf-ispmdb clip"})
            if not title_tag:
                continue
            title = title_tag.text.strip()

            sector_block = card.find("div", string="Sector")
            if not sector_block:
                continue

            value_container = sector_block.find_next_sibling("div")
            if value_container:
                value_text = value_container.text.strip()

                # ➤ Negative or Positive
                class_list = value_container.get("class", [])
                if any("negative" in c for c in class_list):
                    value_text = "-" + value_text
                elif any("positive" in c for c in class_list):
                    value_text = "+" + value_text

                returns[title] = value_text

        except Exception as e:
            print("⚠️ Error parsing returns:", e)
            continue

    # Collect the extra data
    # Find blocks
    extra_blocks = soup.find_all("div", class_="item sector yf-3v3d6w")
    extra_data = {}

    for block in extra_blocks:
        try:
            label = block.find("div", class_="label yf-3v3d6w").text.strip()
            value = block.find("div", class_="value yf-3v3d6w").text.strip()
            extra_data[label] = value
        except Exception as e:
            print("⚠️ Error parsing extra data:", e)
            continue


    # ➤ Εμφανίζουμε τα αποτελέσματα
    print("📊 Returns:")
    for label, value in returns.items():
        print(f"{label}: {value}")
    print("\n📦 Extra Data :")
    for label, value in extra_data.items():
        print(f"{label}: {value}")

    #Data Transforamtion
    clean_returns = {}
    clean_extras = {}

    for key, value in returns.items():
        clean_returns[key] = convert_percentage(value)

    for key, value in extra_data.items():
        if key == "Market Cap":
            clean_extras[key] = convert_market_cap(value)
        elif key == "Market Weight":
            clean_extras[key] = convert_percentage(value)
        elif key in ["Industries", "Companies"]:
            clean_extras[key] = convert_integer(value)
        else:
            clean_extras[key] = value  # default

    print("📉 Returns (Decimal):")
    for k, v in clean_returns.items():
        print(f"{k}: {v}")
    print("📦 Extra (Converted):")
    for k, v in clean_extras.items():
        print(f"{k}: {v}")

    # Save Data
    cursor = conn.cursor()
    date_today = datetime.today().strftime("%Y-%m-%d")

    if type.lower() == "sector":
        sql = """
        INSERT INTO SectorData (
            SectorId, Date, DayReturn, YTDReturn, "1YearReturn", "3YearReturn", "5YearReturn",
            MarketCap, MarketWeight, Industries, Companies
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            id, date_today,
            clean_returns.get("Day Return"),
            clean_returns.get("YTD Return"),
            clean_returns.get("1-Year Return"),
            clean_returns.get("3-Year Return"),
            clean_returns.get("5-Year Return"),
            clean_extras.get("Market Cap"),
            clean_extras.get("Market Weight"),
            clean_extras.get("Industries"),
            clean_extras.get("Companies")
        )
        cursor.execute(sql, values)
        conn.commit()
        print("✅ Sector data saved.")

    elif type.lower() == "industry":
        # Αν έχεις αντίστοιχο πίνακα για Industry, προσαρμόζεις αυτό:
        sql = """
        INSERT INTO IndustryData (
            IndustryId, Date, DayReturn, YTDReturn, "1YearReturn", "3YearReturn", "5YearReturn",
            MarketCap, MarketWeight, Industries, Companies
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            id, date_today,
            clean_returns.get("Day Return"),
            clean_returns.get("YTD Return"),
            clean_returns.get("1-Year Return"),
            clean_returns.get("3-Year Return"),
            clean_returns.get("5-Year Return"),
            clean_extras.get("Market Cap"),
            clean_extras.get("Market Weight"),
            clean_extras.get("Industries"),
            clean_extras.get("Companies")
        )
        cursor.execute(sql, values)
        conn.commit()
        print("✅ Industry data saved.")
