
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import os
import time

# Headless Mode
options = Options()
options.add_argument("--headless=new")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print("Opening CoinMarketCap...")

driver.get("https://coinmarketcap.com/")
time.sleep(15)

rows = driver.find_elements(By.XPATH, "//tbody/tr")

print("Rows Found:", len(rows))

coin_names = [
    "Bitcoin",
    "Ethereum",
    "Tether",
    "BNB",
    "USDC",
    "XRP",
    "Solana",
    "Dogecoin",
    "TRON",
    "Cardano"
]

coins = []

for i, row in enumerate(rows[:10]):
    try:
        cols = row.find_elements(By.TAG_NAME, "td")

        coin_name = coin_names[i]

        price = cols[3].text

        change_24h = cols[4].text

        market_cap = cols[7].text

        coins.append({
            "Coin": coin_name,
            "Price": price,
            "24h Change": change_24h,
            "Market Cap": market_cap,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        print(
            coin_name,
            price,
            change_24h,
            market_cap
        )

    except Exception as e:
        print("Error:", e)

os.makedirs("data", exist_ok=True)

df = pd.DataFrame(coins)

df.to_csv(
    "data/crypto_data.csv",
    index=False
)

print("\nCSV File Saved Successfully")

print(df)

driver.quit()