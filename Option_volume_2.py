import yfinance as yf

tickers = ["XYL", "XPO", "XOM", "XNCR", "XENE", "XEL", "WYNN", "WWW", "WTRG", "WRBY"]
exp_date = "2026-11-20"
matches = []

for t in tickers:
    try:
        tk = yf.Ticker(t)
        if exp_date in tk.options:
            calls = tk.option_chain(exp_date).calls
            if (calls["volume"].fillna(0) > 100).any():
                matches.append(t)
    except Exception:
        pass

print(", ".join(matches))
