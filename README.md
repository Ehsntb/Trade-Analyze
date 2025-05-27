# 📊 Crypto Trade Analyzer Bot

A real-time Telegram bot for scalping and futures trading, designed to analyze cryptocurrencies like **Bitcoin (BTC)** and **Ethereum (ETH)** using a combination of advanced technical indicators and price action strategies.

---

## 🚀 Features

- ✅ Multi-indicator signal analysis
  - RSI, MACD, EMA crossovers
  - Candlestick patterns
  - Volume comparison
  - Break of structure (BoS)
  - Supply & Demand Zones
  - Harmonic Patterns (ABCD)
  - Elliott Wave detection
  - RTM (Smart Money concept)

- 💡 Signal Ratings:
  - Strong Buy / Buy / Neutral / Sell / Strong Sell
  - Watch mode when partial confirmations are met

- 🎯 Trade Plan Output:
  - Live market price
  - Entry price
  - Target and Stop Loss (auto-calculated)

- 🔔 Auto-analysis:
  - Scheduled analysis every 2 minutes
  - Sends real-time alerts only if profitable signal is found

- 🔧 User control:
  - Custom notification toggle per user
  - Telegram inline keyboard for selecting symbols

---

## 🛠 Project Structure

```
Trade-Analyze/
├── analyzer/
│   ├── __init__.py
│   ├── core.py
│   ├── patterns.py
│   ├── rsi_macd_ema.py
│   ├── volume.py
│   ├── bos.py
│   ├── supply_demand.py
│   ├── harmonic.py
│   ├── elliott_wave.py
│   ├── trade_plan.py
├── utils/
│   ├── __init__.py
│   ├── fetch_data.py
├── user_config.py
├── main.py
├── keep_alive.py
├── requirements.txt
├── .env
└── README.md
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Ehsntb/Trade-Analyze.git
cd Trade-Analyze
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
Create a `.env` file:
```
BOT_TOKEN=your_telegram_bot_token
```

### 4. Run the Bot
```bash
python main.py
```

---

## 💬 Telegram Commands

- `/start` → Show symbol keyboard
- Tap on 🟠 BTC/USDT, 🔵 ETH/USDT, or others to receive instant analysis
- `/signal BTCUSDT` → Manual signal request

---

## 📡 Auto Analysis (Optional)

To keep the bot alive on free hosting (e.g., Replit), use **UptimeRobot** or similar service to ping your endpoint every 5 minutes.

---

## 📬 Contact

**Developer:** [Ehsan Tabatabaei](https://github.com/Ehsntb)  
For business or contributions, feel free to reach out via Telegram or GitHub Issues.

---

## 🏷 License

This project is open-source under the **MIT License**.