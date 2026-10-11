# Workshop 1 — EUR/USD Indicator Lab

This worksheet walks through a small, reproducible historical-data research project on a Windows PC. It is designed for a beginner and should take about an hour for the first pass.

## What we are trying to learn

Yes: ultimately, we want to know whether simple indicator-based trading rules would have made or lost money on historical EUR/USD data. We will work in stages so that we do not confuse an indicator describing the market with a strategy that can actually be traded profitably.

1. **Explore indicators:** calculate moving averages, RSI, momentum and volatility.
2. **Study subsequent returns:** ask what EUR/USD did over the next 1, 5 and 20 trading days after different indicator readings.
3. **Define simple rules:** for example, buy when the 20-day moving average crosses above the 50-day moving average and exit when it crosses below.
4. **Calculate hypothetical profit and loss (P/L):** apply the rule to historical prices and record the result.
5. **Make the test more realistic:** account for bid/ask spread, commissions where relevant, slippage and the fact that a signal is only known after a candle closes.
6. **Check robustness:** reserve later data for a final out-of-sample check rather than judging a rule only on the data used to explore it.

This is an educational historical simulation, not evidence that a strategy will work in future markets.

## Research boundaries

- Use historical daily EUR/USD data only for this first workshop.
- Do not connect to a broker or place live orders.
- Do not use leverage or assume that costs are zero in the P/L stage.
- Do not repeatedly adjust indicator settings until the historical result looks good. That can overfit the past.
- Keep a record of assumptions, code changes and results so the experiment can be repeated.

## Tools

The project uses Python and common free data-analysis libraries. The repository's README describes the intended stack: Windows Terminal or PowerShell, Git, Python tooling, pandas/NumPy, and matplotlib. Data access is via Yahoo Finance (ticker **EURUSD=X**) for this introductory exercise; availability and historical data quality should be checked rather than assumed.

## Step 1 — Set up the project

Open PowerShell in your local copy of the repository. If you have not cloned it yet, use:

    git clone https://github.com/pimm43/forex-trading.git
    cd forex-trading

Install Python and the project tools as described in the README. If using uv, create an environment and add the required packages:

    uv init
    uv add yfinance pandas numpy matplotlib

If the repository already contains a Python project file when you start, do not run uv init over it; simply install its declared dependencies.

## Step 2 — Download and inspect EUR/USD prices

Use the Yahoo Finance ticker **EURUSD=X** and download daily data over a clearly recorded date range. Inspect the first and last rows, missing values, duplicate dates, and whether the downloaded columns contain usable prices. Keep a note of the download date and date range.

For this exercise, the close price is the starting point for calculations. In real FX trading, the price at which you can buy is not the same as the price at which you can sell.

## Step 3 — Calculate the indicators

Calculate the following from daily close prices:

- **20-day simple moving average (SMA):** average close over the latest 20 trading sessions.
- **50-day SMA:** average close over the latest 50 trading sessions.
- **14-day RSI:** a common momentum oscillator, conventionally shown on a 0–100 scale.
- **20-day momentum:** today's close divided by the close 20 sessions earlier, minus one.
- **20-day rolling annualised volatility:** standard deviation of daily returns over 20 sessions, multiplied by the square root of 252.

The first rows will be blank where there is not enough history to calculate an indicator. That is expected; do not fill these rows with invented values.

## Step 4 — Explore future returns (not yet strategy P/L)

For each date where the data permits, calculate the subsequent 1-, 5- and 20-session close-to-close returns. Group or compare those returns by simple conditions, such as:

- 20-day SMA above or below the 50-day SMA.
- RSI below 30, between 30 and 70, or above 70.
- Positive or negative 20-day momentum.
- Lower or higher rolling volatility.

Ask: how many observations are in each group? What is the average and median future return? How widely do returns vary? Are the differences large enough to be meaningful, or could they be noise?

**Important:** the indicator reading must use information available on the signal date only. Do not use future prices to calculate a signal.

## Step 5 — Define a basic trading rule

As a first example, test a moving-average crossover:

- **Entry:** when the 20-day SMA crosses from at-or-below to above the 50-day SMA, enter a hypothetical long position at the next session's open, if open prices are available.
- **Exit:** when the 20-day SMA crosses from at-or-above to below the 50-day SMA, exit at the next session's open.
- **Position:** one unit of EUR/USD for a simple return-based illustration; position sizing and account currency conversion can be added later.
- **No look-ahead:** the crossover is determined using completed daily candles; execution happens only after that information is available.

This is one example to learn the mechanics, not a recommended trading strategy. A long-only rule can be compared with simply holding EUR/USD over the same period.

## Step 6 — Calculate hypothetical P/L

Record each trade's entry date and price, exit date and price, gross return, estimated costs and net return. Also calculate:

- Total cumulative return and total net P/L under a clearly stated starting capital and position-size assumption.
- Number of trades, winning trades, losing trades and win rate.
- Average win, average loss and expectancy per trade.
- Maximum drawdown: the largest peak-to-trough decline in the cumulative equity curve.
- Exposure: how much of the test period the strategy was in the market.
- A comparison with a simple buy-and-hold benchmark.

For a long trade, the simple gross price return is (exit price / entry price) - 1. This is not automatically the account-currency P/L for a leveraged retail FX position. Actual P/L depends on position size, quote/base currency, account currency, financing/swap, spread, commissions and execution.

Subtract realistic transaction costs before interpreting the result. If historical bid/ask data are not available, label any assumed spread clearly and test how the conclusion changes under higher costs. A backtest with no costs is only a preliminary upper-bound illustration.

## Step 7 — Check the result honestly

- Plot EUR/USD close, moving averages, entries/exits and the cumulative strategy return.
- Check that signals and fills are aligned in time and no future information leaks into the rules.
- Separate an earlier exploratory period from a later test period.
- Report negative results as well as positive ones.
- Avoid changing the rule based on the test period and then presenting that same period as independent validation.

A positive historical result does not establish a future edge. A negative result is still useful: it tells us that this simple rule did not work under the assumptions tested.

## Results log

| Item | Record |
|---|---|
| Data source and ticker | e.g. Yahoo Finance, EURUSD=X |
| Download date and tested dates | Exact dates |
| Rule and indicator settings | Exact conditions and periods |
| Execution assumption | Signal close / next open, etc. |
| Cost assumption | Spread, commission, slippage |
| Number of trades | Count |
| Gross and net return / P&L | State units, capital and position size |
| Maximum drawdown | Percentage and dates |
| Benchmark result | Same period |
| Notes | Data issues, limitations, next question |

## Next step

After completing this worksheet, create a small Python script that downloads the data, calculates the indicators, prints the exploratory statistics and saves charts. Only after those outputs are checked should we add a separate backtest module for trade-by-trade P/L.
