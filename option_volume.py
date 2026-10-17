import pandas as pd
import yfinance as yf

def scan_sp500_atm_calls():
    # 1. Fetch S&P 500 Ticker List
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    sp500_df = tables[0]
    tickers = sp500_df['Symbol'].str.replace('.', '-', regex=False).tolist()
    
    target_exp = "2026-08-21"
    matching_tickers = []

    print(f"Scanning S&P 500 ATM calls for expiration date: {target_exp}...\n")

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            
            # Verify target expiration exists
            if target_exp not in stock.options:
                continue
                
            # Get latest closing stock price
            hist = stock.history(period="2d")
            if hist.empty:
                continue
            close_price = hist['Close'].iloc[-1]
            
            # Fetch Call option chain
            chain = stock.option_chain(target_exp)
            calls = chain.calls.copy()
            
            if calls.empty:
                continue
            
            # Find the At-The-Money (ATM) Call strike
            calls['strike_diff'] = (calls['strike'] - close_price).abs()
            atm_call = calls.loc[calls['strike_diff'].idxmin()]
            
            call_vol = atm_call['volume'] if pd.notna(atm_call['volume']) else 0
            
            # Filter for ATM Call Volume > 100
            if call_vol > 100:
                matching_tickers.append({
                    'Ticker': ticker,
                    'Close Price': round(close_price, 2),
                    'ATM Strike': atm_call['strike'],
                    'ATM Call Volume': int(call_vol),
                    'ATM Call Open Interest': int(atm_call['openInterest']) if pd.notna(atm_call['openInterest']) else 0
                })
                print(f"Match found: {ticker} | Strike: {atm_call['strike']} | Call Vol: {int(call_vol)}")
                
        except Exception:
            continue

    results_df = pd.DataFrame(matching_tickers)
    return results_df

# Run Scan and display top results
results = scan_sp500_atm_calls()
print("\n--- Final Filtered Results ---")
print(results)
