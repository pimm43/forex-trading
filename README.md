# Workshop 1 — EUR/USD Indicator Lab

## Purpose

This introductory workshop builds a small, reproducible quantitative-research workflow on a Windows PC using free tools.

The project currently has two stages:

1. **Indicator exploration** — calculate indicators and examine subsequent returns.
2. **A first strategy backtest** — test a simple SMA20/SMA50 crossover with next-open execution and an adjustable assumed spread.

The goal is to learn how to test claims reproducibly. This is historical research, not a live trading system.

## Stack

- Windows Terminal / PowerShell
- Git for Windows
- Python
- `yfinance` for introductory EUR/USD daily data
- pandas / NumPy
- matplotlib

## Stage 1: Explore indicators

The first experiment uses daily **EUR/USD** data and calculates:

- 20-day moving average
- 50-day moving average
- 14-day RSI
- 20-day momentum
- 20-day rolling annualised volatility

It then examines future 1-day, 5-day and 20-day returns and asks simple questions about trend, momentum, RSI and volatility.

The research script is **[indicator_lab.py](./indicator_lab.py)**.

## Stage 2: Test a simple strategy

The new **[strategy_backtest.py](./strategy_backtest.py)** script tests a basic rule:

- If the 20-day SMA is above the 50-day SMA, hold a hypothetical long position.
- If the 20-day SMA is at or below the 50-day SMA, hold a hypothetical short position.
- The signal is calculated from a daily close and applied at the following day's open.
- Performance is measured from one daily open to the next daily open, so the strategy does not use a signal before it was available.
- An estimated spread is charged when the position changes. The default full spread is 1.0 pip, split across entry and exit.

This is a deliberately simple baseline, not a recommendation to trade this rule. It is not a scalping test and does not model account currency, lot size, leverage, swaps/financing, variable spreads, slippage, commissions, margin calls or broker execution details.

## Run the project on Windows

After cloning the repository, open PowerShell in the project folder.

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation scripts, this command permits activation only for the current PowerShell session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run indicator exploration:

```powershell
python indicator_lab.py
```

Run the SMA crossover backtest:

```powershell
python strategy_backtest.py
```

To test a different data period or assumed spread:

```powershell
python strategy_backtest.py --period 5y --spread-pips 1.5
```

## Output files

The scripts create an `output` folder.

Indicator exploration creates:

- `eurusd_indicators.csv` — prices, indicator values and future returns
- `forward_return_summary.csv` — grouped return statistics
- `eurusd_moving_averages.png` — price and moving-average chart

The strategy backtest creates:

- `eurusd_sma_backtest.csv` — daily positions, returns, estimated costs and equity indices
- `eurusd_sma_backtest_summary.csv` — headline performance statistics

## How to interpret the backtest

Review net return alongside maximum drawdown, annualised return, the buy-and-hold comparison and the assumed spread. A positive historical return alone does not prove a strategy is reliable. Results can change with data source, execution assumptions and costs. Any promising rule should be checked on a separate out-of-sample period before drawing conclusions.

## Important boundary

This workshop is for **research and education only**. It does not connect to a broker or place trades. The backtest is a simplified hypothetical model and does not calculate actual broker account P/L or guarantee future performance.
