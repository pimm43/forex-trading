# Workshop 1 — EUR/USD Indicator Lab

## Purpose

This introductory workshop builds a small, reproducible quantitative-research workflow on a Windows PC using free tools.

By the end of the workshop, you should be able to:

```text
download EUR/USD daily data
→ calculate a few simple indicators
→ test simple hypotheses
→ generate charts and results
→ inspect the code changes
→ commit the work with Git
→ push the project to GitHub
```

The workshop is designed to be completed in roughly **one hour** on an ordinary Windows PC or 32 GB mini-PC.

## Stack

- Windows Terminal / PowerShell
- Git for Windows
- Python
- `uv` or pip for package management
- `yfinance` for introductory EUR/USD daily data
- pandas / NumPy
- matplotlib

No paid AI subscription is required for the local workflow.

## First experiment

The first experiment uses daily **EUR/USD** data and calculates:

- 20-day moving average
- 50-day moving average
- 14-day RSI
- 20-day momentum
- 20-day rolling annualised volatility

It then examines future 1-day, 5-day and 20-day returns and asks simple questions about trend, momentum, RSI and volatility.

The purpose is **not** to optimise a trading strategy. The purpose is to establish a clean research pipeline and learn how to test claims reproducibly. A separate backtest for hypothetical profit/loss will follow after the data and exploratory results have been checked.

## Run the workshop

See **[WORKSHEET.md](./WORKSHEET.md)** for the step-by-step exercise.

The first research script is **[indicator_lab.py](./indicator_lab.py)**. It downloads daily EUR/USD data, calculates the indicators, creates a forward-return summary, and saves a price chart.

### Quick start on Windows

Install Python and Git, then open PowerShell and clone the repository:

```powershell
git clone https://github.com/pimm43/forex-trading.git
cd forex-trading
```

Using `uv`:

```powershell
uv init
uv add yfinance pandas numpy matplotlib
uv run python indicator_lab.py
```

If the repository already has a `pyproject.toml` when you clone it, do not run `uv init` again; just install the dependencies listed in that file.

Alternatively, with a standard Python installation:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py indicator_lab.py
```

The script writes these files to an `output` folder:

- `eurusd_indicators.csv` — prices, indicator values and future returns
- `forward_return_summary.csv` — grouped return statistics
- `eurusd_moving_averages.png` — price and moving-average chart

You can request a different Yahoo Finance history period, for example:

```powershell
py indicator_lab.py --period 5y
```

## Important boundary

This workshop is for **research and education only**. The script does not connect to a broker, place trades, model leverage, or calculate account-currency trading P/L. Forward returns are exploratory statistics, not proof of a profitable strategy. A later backtest must specify entry/exit timing, position sizing, transaction costs and drawdown, and should be checked on data not used to develop the rule.
