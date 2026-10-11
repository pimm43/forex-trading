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
- GitHub CLI
- `uv` for Python and package management
- Python
- Ollama for local LLM inference
- a local coding model
- OpenCode as the terminal coding agent
- `yfinance` for introductory EUR/USD daily data
- pandas / NumPy
- SciPy / statsmodels
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

The purpose is **not** to optimise a trading strategy. The purpose is to establish a clean research pipeline and learn how to test claims reproducibly.

## Important boundary

This workshop is for **research and education only**.

It does not include:

- broker integration
- automated execution
- leverage
- live trading
- parameter optimisation for profit
- financial advice

## Run the workshop

See:

**[WORKSHEET.md](./WORKSHEET.md)**

for the full step-by-step exercise.
