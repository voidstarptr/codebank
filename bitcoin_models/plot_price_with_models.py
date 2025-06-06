import argparse
from datetime import datetime
import requests
import matplotlib.pyplot as plt


API_URL = 'https://api.coingecko.com/api/v3/coins/bitcoin/history'

def fetch_price(date_str: str) -> float:
    """Fetch Bitcoin price for a specific date (UTC) from CoinGecko."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted = date_obj.strftime('%d-%m-%Y')
    params = {'date': formatted, 'localization': 'false'}
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data['market_data']['current_price']['usd']


def stock_to_flow_price(date_obj: datetime) -> float:
    """Simplified Stock-to-Flow prediction for the given date."""
    days = (date_obj - datetime(2012, 11, 28)).days / 365.25
    s2f_ratio = 3 * (2 ** (days / 4))
    return 1000 * s2f_ratio


def rainbow_band(date_obj: datetime) -> tuple[float, float]:
    """Return low/high rainbow band prices for the given date."""
    days = (date_obj - datetime(2012, 1, 1)).days
    log_price = 0.0008 * days + 2
    low = 10 ** (log_price - 0.3)
    high = 10 ** (log_price + 0.3)
    return low, high


def power_law_band(date_obj: datetime) -> tuple[float, float]:
    """Return a simple power law corridor for the given date."""
    age = (date_obj - datetime(2009, 1, 3)).days
    base = age ** 0.5
    low = 0.4 * base ** 4
    high = 1.6 * base ** 4
    return low, high


def plot_predictions(date_str: str, price: float, s2f: float,
                      rainbow_low: float, rainbow_high: float,
                      power_low: float, power_high: float) -> None:
    models = ['S2F', 'Rainbow Low', 'Rainbow High', 'Power Low', 'Power High']
    values = [s2f, rainbow_low, rainbow_high, power_low, power_high]
    colors = ['tab:blue', 'tab:green', 'tab:green', 'tab:orange', 'tab:orange']

    plt.figure(figsize=(8, 5))
    plt.bar(models, values, color=colors, alpha=0.7, label='Model prediction')
    plt.axhline(price, color='red', linestyle='--', label=f'Actual price {price:.2f} USD')
    plt.ylabel('Price (USD)')
    plt.title(f'Bitcoin price on {date_str}')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('bitcoin_price_{}.png'.format(date_str))
    print(f"Saved plot to bitcoin_price_{date_str}.png")


def main() -> None:
    parser = argparse.ArgumentParser(description='Bitcoin price vs prediction models')
    parser.add_argument('--date', required=True, help='Date in YYYY-MM-DD format')
    args = parser.parse_args()

    dt = datetime.strptime(args.date, '%Y-%m-%d')
    price = fetch_price(args.date)
    s2f = stock_to_flow_price(dt)
    rainbow_low, rainbow_high = rainbow_band(dt)
    power_low, power_high = power_law_band(dt)

    plot_predictions(args.date, price, s2f, rainbow_low, rainbow_high, power_low, power_high)


if __name__ == '__main__':
    main()
