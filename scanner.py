import os
import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime
from telegram.ext import Application
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TARGET_PRICE = 250
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Retailers configuration
RETAILERS = {
    'Bergfreunde': {
        'url': 'https://www.bergfreunde.nl/arcteryx-beta-lt-jacket-m-hardshell-jacket/',
        'selector': 'span[class*="product-price"]',
        'price_cleanup': lambda x: float(x.replace('€', '').replace(',', '.').strip())
    },
    'Zwerfkei': {
        'url': 'https://www.zwerfkei.nl/arcteryx-beta-lt-jacket-men-s.html',
        'selector': 'span.price',
        'price_cleanup': lambda x: float(x.replace('€', '').replace(',', '.').strip())
    },
    'Snowleader': {
        'url': 'https://www.snowleader.nl/beta-lt-jacket-men-s.html',
        'selector': 'span.price',
        'price_cleanup': lambda x: float(x.replace('€', '').replace(',', '.').strip())
    },
    'Coef': {
        'url': 'https://coef.nl/arcteryx-beta-lt-jacket-men/',
        'selector': 'p.price',
        'price_cleanup': lambda x: float(x.replace('€', '').replace(',', '.').strip())
    },
    'Bever': {
        'url': 'https://www.bever.nl/p/arcteryx-beta-lt-jacket-heren-HABAA4000X.html',
        'selector': 'span[data-price]',
        'price_cleanup': lambda x: float(x.replace('€', '').replace(',', '.').strip())
    }
}

# Headers to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

async def send_telegram_message(message):
    """Send message via Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram configuration missing. Skipping notification.")
        return
    
    try:
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        await app.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def check_price(retailer_name, config):
    """Check price for a specific retailer."""
    try:
        response = requests.get(config['url'], headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.select_one(config['selector'])
        
        if price_element:
            price_text = price_element.text
            price = config['price_cleanup'](price_text)
            
            print(f"{retailer_name}: €{price}")
            
            if price <= TARGET_PRICE:
                message = (
                    f"🎉 Deal Alert! 🎉\n"
                    f"Arc'teryx Beta LT Jacket found at {retailer_name}\n"
                    f"Price: €{price}\n"
                    f"URL: {config['url']}"
                )
                return message
        
    except Exception as e:
        print(f"Error checking {retailer_name}: {e}")
    
    return None

def scan_all_retailers():
    """Scan all retailers for prices."""
    print(f"\nScanning retailers at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    notifications = []
    for retailer_name, config in RETAILERS.items():
        result = check_price(retailer_name, config)
        if result:
            notifications.append(result)
    
    if notifications:
        message = "\n\n".join(notifications)
        import asyncio
        asyncio.run(send_telegram_message(message))

def main():
    """Main function to run the price scanner."""
    print("Arc'teryx Beta LT Jacket Price Scanner")
    print("=====================================")
    print(f"Target price: €{TARGET_PRICE}")
    
    # Run immediately on start
    scan_all_retailers()
    
    # Schedule to run every 3 hours
    schedule.every(3).hours.do(scan_all_retailers)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()