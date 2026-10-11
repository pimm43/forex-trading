"""
EUR/USD Indicator Lab
---------------------
Downloads daily EUR/USD prices, calculates basic indicators, compares subsequent
returns, and saves CSV files plus a chart.

This is historical research only. It does not place trades or calculate broker P/L.
"""

from pathlib import Path
import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf


OUTPUT_DIR = Path("output")


def download_prices(period: str) -> pd.DataFrame:
    """Download daily EUR/USD prices and return a clean OHLCV DataFrame."""
    data = yf.download(
        "EURUSD=X",
        period=period,
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if data.empty:
        raise RuntimeError(
            "No price data was downloaded. Check your internet connection, "
            "Yahoo Finance availability, and the ticker EURUSD=X."
        )

    # Recent yfinance versions may return a MultiIndex column layout.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data.columns = [str(column).title() for column in data.columns]
    data.index = pd.to_datetime(data.index)
    data = data[~data.index.duplicated(keep="first")].sort_index()

    if "Close" not in data.columns:
        raise RuntimeError(f"Expected a Close column; received: {list(data.columns)}")

    data = data.dropna(subset=["Close"])
    if len(data) < 60:
        raise RuntimeError(
            f"Only {len(data)} usable rows were downloaded; at least 60 are needed."
        )
    return data


def calculate_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Add indicators and forward returns without filling unavailable values."""
    result = data.copy()
    close = result["Close"]

    result["SMA_20"] = close.rolling(window=20).mean()
    result["SMA_50"] = close.rolling(window=50).mean()

    change = close.diff()
    gains = change.clip(lower=0)
    losses = -change.clip(upper=0)
    average_gain = gains.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    average_loss = losses.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    relative_strength = average_gain / average_loss.replace(0, np.nan)
    result["RSI_14"] = 100 - (100 / (1 + relative_strength))

    result["Momentum_20"] = close / close.shift(20) - 1
    daily_returns = close.pct_change()
    result["Volatility_20_Annualised"] = (
        daily_returns.rolling(window=20).std() * np.sqrt(252)
    )

    for horizon in (1, 5, 20):
        result[f"Forward_Return_{horizon}d"] = close.shift(-horizon) / close - 1

    # Labels make the exploratory group summaries easier to read.
    result["SMA_Trend"] = np.where(
        result["SMA_20"] > result["SMA_50"], "20-day SMA above 50-day SMA",
        "20-day SMA at/below 50-day SMA"
    )
    result["RSI_Group"] = pd.cut(
        result["RSI_14"],
        bins=[-np.inf, 30, 70, np.inf],
        labels=["RSI below 30", "RSI 30 to 70", "RSI above 70"],
        right=True,
    )
    result["Momentum_Group"] = np.where(
        result["Momentum_20"] > 0, "Positive 20-day momentum",
        "Zero or negative 20-day momentum"
    )
    volatility_median = result["Volatility_20_Annualised"].median()
    result["Volatility_Group"] = np.where(
        result["Volatility_20_Annualised"] > volatility_median,
        "Above-median volatility",
        "At/below-median volatility",
    )
    return result


def create_return_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Summarise forward returns for simple indicator groups."""
    grouping_columns = [
        "SMA_Trend", "RSI_Group", "Momentum_Group", "Volatility_Group"
    ]
    rows = []

    for group_column in grouping_columns:
        for group_name, group in data.groupby(group_column, observed=False, dropna=True):
            for horizon in (1, 5, 20):
                column = f"Forward_Return_{horizon}d"
                values = group[column].dropna()
                if values.empty:
                    continue
                rows.append({
                    "Indicator_Group": group_column,
                    "Group": str(group_name),
                    "Horizon_Days": horizon,
                    "Observations": int(values.count()),
                    "Average_Forward_Return": float(values.mean()),
                    "Median_Forward_Return": float(values.median()),
                    "Positive_Return_Percent": float((values > 0).mean() * 100),
                })

    return pd.DataFrame(rows)


def save_chart(data: pd.DataFrame, path: Path) -> None:
    """Save a price and moving-average chart."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data["Close"], label="EUR/USD close", linewidth=1)
    ax.plot(data.index, data["SMA_20"], label="20-day SMA", linewidth=1)
    ax.plot(data.index, data["SMA_50"], label="50-day SMA", linewidth=1)
    ax.set_title("EUR/USD Daily Close and Moving Averages")
    ax.set_xlabel("Date")
    ax.set_ylabel("Exchange rate (USD per EUR)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Explore EUR/USD indicators and subsequent historical returns."
    )
    parser.add_argument(
        "--period",
        default="10y",
        help="Yahoo Finance history period, for example 5y, 10y, or max (default: 10y).",
    )
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading daily EUR/USD data (period={args.period})...")
    prices = download_prices(args.period)
    results = calculate_indicators(prices)
    summary = create_return_summary(results)

    data_path = OUTPUT_DIR / "eurusd_indicators.csv"
    summary_path = OUTPUT_DIR / "forward_return_summary.csv"
    chart_path = OUTPUT_DIR / "eurusd_moving_averages.png"

    results.to_csv(data_path, index_label="Date")
    summary.to_csv(summary_path, index=False)
    save_chart(results, chart_path)

    print()
    print(f"Data rows: {len(results)}")
    print(f"Date range: {results.index.min().date()} to {results.index.max().date()}")
    print(f"Files saved in: {OUTPUT_DIR.resolve()}")
    print(f" - {data_path.name}")
    print(f" - {summary_path.name}")
    print(f" - {chart_path.name}")
    print()
    print("Forward-return summary (returns are percentages):")
    display_columns = [
        "Indicator_Group", "Group", "Horizon_Days", "Observations",
        "Average_Forward_Return", "Median_Forward_Return",
        "Positive_Return_Percent",
    ]
    if not summary.empty:
        display = summary.copy()
        for column in [
            "Average_Forward_Return", "Median_Forward_Return"
        ]:
            display[column] = display[column] * 100
        display["Positive_Return_Percent"] = display["Positive_Return_Percent"].round(1)
        print(display[display_columns].round(3).to_string(index=False))
    else:
        print("No grouped results were available; inspect the downloaded data.")

    print()
    print("Reminder: these are exploratory future-return statistics, not strategy P/L.")
    print("Trading costs, position sizing, execution assumptions and drawdown are not yet modelled.")


if __name__ == "__main__":
    main()
