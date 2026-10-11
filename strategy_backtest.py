"""
EUR/USD SMA crossover backtest
------------------------------
Educational daily-data backtest. The signal is calculated from the prior day's
close and executed at the next day's open, avoiding use of future information.

This is not broker P/L: it does not model leverage, financing, variable spreads,
slippage, commissions, lot sizing, or margin calls.
"""

from pathlib import Path
import argparse

import numpy as np
import pandas as pd

from indicator_lab import calculate_indicators, download_prices

OUTPUT_DIR = Path("output")
PIP_SIZE = 0.0001  # EUR/USD: one pip is 0.0001


def run_backtest(period: str, spread_pips: float) -> tuple[pd.DataFrame, dict]:
    prices = calculate_indicators(download_prices(period))

    if "Open" not in prices.columns:
        raise RuntimeError("Downloaded data has no Open column; cannot model next-open execution.")

    # Signal known after each daily close: long if SMA20 > SMA50, otherwise short.
    signal = pd.Series(np.nan, index=prices.index, dtype=float)
    ready = prices["SMA_20"].notna() & prices["SMA_50"].notna()
    signal.loc[ready] = np.where(
        prices.loc[ready, "SMA_20"] > prices.loc[ready, "SMA_50"], 1.0, -1.0
    )

    # A signal from the previous close is held from today's open to the next open.
    position = signal.shift(1)
    next_open_return = prices["Open"].shift(-1) / prices["Open"] - 1.0

    backtest = pd.DataFrame({
        "Open": prices["Open"],
        "SMA_20": prices["SMA_20"],
        "SMA_50": prices["SMA_50"],
        "Signal_After_Close": signal,
        "Position_For_Open_To_Open_Interval": position,
        "Open_To_Next_Open_Return": next_open_return,
    })
    backtest = backtest.dropna(
        subset=["Position_For_Open_To_Open_Interval", "Open_To_Next_Open_Return"]
    ).copy()

    # A full spread is split across entry/exit. A reversal changes position by 2,
    # so it pays the equivalent of closing one side and opening the other.
    turnover = backtest["Position_For_Open_To_Open_Interval"].diff().abs()
    if not turnover.empty:
        turnover.iloc[0] = abs(backtest["Position_For_Open_To_Open_Interval"].iloc[0])
    cost_fraction = (
        turnover * (spread_pips / 2.0) * PIP_SIZE / backtest["Open"]
    )

    backtest["Gross_Strategy_Return"] = (
        backtest["Position_For_Open_To_Open_Interval"] * backtest["Open_To_Next_Open_Return"]
    )
    backtest["Estimated_Cost"] = cost_fraction
    backtest["Net_Strategy_Return"] = (
        backtest["Gross_Strategy_Return"] - backtest["Estimated_Cost"]
    )
    backtest["Strategy_Equity_Index"] = (1.0 + backtest["Net_Strategy_Return"]).cumprod()

    # Buy-and-hold benchmark uses the same open-to-next-open intervals.
    backtest["Buy_Hold_Equity_Index"] = (1.0 + backtest["Open_To_Next_Open_Return"]).cumprod()

    net = backtest["Net_Strategy_Return"]
    equity = backtest["Strategy_Equity_Index"]
    years = max(
        (backtest.index[-1] - backtest.index[0]).days / 365.25,
        1 / 365.25,
    )
    total_return = float(equity.iloc[-1] - 1.0)
    cagr = float(equity.iloc[-1] ** (1.0 / years) - 1.0) if equity.iloc[-1] > 0 else float("nan")
    drawdown = equity / equity.cummax() - 1.0
    daily_std = float(net.std(ddof=1))
    sharpe = float((net.mean() / daily_std) * np.sqrt(252)) if daily_std > 0 else float("nan")
    changes = int((turnover > 0).sum())

    summary = {
        "Start_Date": str(backtest.index[0].date()),
        "End_Date": str(backtest.index[-1].date()),
        "Intervals": int(len(backtest)),
        "Assumed_Spread_Pips": float(spread_pips),
        "Position_Changes": changes,
        "Gross_Strategy_Return_Percent": float(backtest["Gross_Strategy_Return"].add(1).prod() * 100 - 100),
        "Net_Strategy_Return_Percent": total_return * 100,
        "Annualised_Net_Return_Percent": cagr * 100,
        "Maximum_Drawdown_Percent": float(drawdown.min() * 100),
        "Buy_Hold_Return_Percent": float((backtest["Buy_Hold_Equity_Index"].iloc[-1] - 1.0) * 100),
        "Profitable_Intervals_Percent": float((net > 0).mean() * 100),
        "Annualised_Sharpe_Ratio": sharpe,
    }
    backtest["Position_Change_Units"] = turnover
    return backtest, summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backtest a daily EUR/USD SMA20/SMA50 crossover with next-open execution."
    )
    parser.add_argument("--period", default="10y", help="Yahoo Finance history period (default: 10y).")
    parser.add_argument(
        "--spread-pips", type=float, default=1.0,
        help="Assumed full EUR/USD spread in pips, split between entry and exit (default: 1.0).",
    )
    args = parser.parse_args()
    if args.spread_pips < 0:
        parser.error("--spread-pips must be zero or greater")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading daily EUR/USD data (period={args.period})...")
    results, summary = run_backtest(args.period, args.spread_pips)

    csv_path = OUTPUT_DIR / "eurusd_sma_backtest.csv"
    summary_path = OUTPUT_DIR / "eurusd_sma_backtest_summary.csv"
    results.to_csv(csv_path, index_label="Date")
    pd.DataFrame([summary]).to_csv(summary_path, index=False)

    print()
    print("Daily SMA20/SMA50 crossover backtest")
    print("------------------------------------")
    for key, value in summary.items():
        if key.endswith("_Percent"):
            print(f"{key.replace('_', ' ')}: {value:.2f}%")
        elif key == "Annualised_Sharpe_Ratio":
            print(f"{key.replace('_', ' ')}: {value:.3f}")
        else:
            print(f"{key.replace('_', ' ')}: {value}")
    print()
    print(f"Saved daily results: {csv_path.resolve()}")
    print(f"Saved summary:       {summary_path.resolve()}")
    print()
    print("Research only: hypothetical returns are not a guarantee of future performance.")
    print("This simple model excludes leverage, swaps/financing, slippage, commissions,")
    print("variable spreads, broker execution rules and account-currency P/L.")


if __name__ == "__main__":
    main()
