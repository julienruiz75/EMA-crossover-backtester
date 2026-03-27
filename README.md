# EMA Crossover Backtesting Framework

A modular Python project for designing, backtesting, and evaluating an **EMA crossover trading strategy** on historical equity data, with transaction costs, performance analytics, signal visualization, and parameter optimization.

---

## Overview

This project implements a complete **trend-following backtesting pipeline** based on the crossover of two **Exponential Moving Averages (EMA)**.

The objective is not simply to plot technical indicators, but to build a structured and reusable research workflow that includes:

- historical market data acquisition
- data cleaning and preprocessing
- indicator computation
- trading signal generation
- realistic position handling with signal shifting
- transaction costs and slippage
- portfolio equity curve construction
- performance metrics computation
- visualization of signals and equity curves
- grid search over multiple EMA parameter combinations

The project was built as a first step toward more advanced **systematic trading** and **quantitative research** workflows.

---

## Project Objective

The core research question behind this project is:

**Can a simple trend-following strategy based on EMA crossovers generate attractive risk-adjusted returns once execution realism and trading frictions are taken into account?**

To answer this, the project tests a **long/flat trading rule**:

- enter the market when the short-term EMA moves above the long-term EMA
- exit the market when the short-term EMA falls below the long-term EMA

This logic is applied to **Apple (AAPL)** historical daily data over a configurable time range.

---

## Strategy Logic

The strategy relies on two exponential moving averages:

- **Short EMA**: captures recent price dynamics
- **Long EMA**: captures the broader market trend

### Trading rule

- **Buy / Hold Long** when `EMA_short > EMA_long`
- **Exit / Stay Flat** when `EMA_short <= EMA_long`

### Important implementation detail

To avoid **look-ahead bias**, the strategy does **not** trade on the same bar where the signal is observed.

Instead:

- the signal is computed at time `t`
- the actual position is applied at time `t+1`

This is a key point in making the backtest more realistic.

---

## Key Features

- **Modular architecture** for research and code readability
- **Historical data download** using `yfinance`
- **EMA-based signal generation**
- **Long/flat backtesting engine**
- **Transaction cost and slippage modeling**
- **Performance analytics**
- **Signal visualization**
- **Equity curve comparison vs buy-and-hold**
- **Parameter optimization** over multiple EMA combinations
- **CSV export** of both enriched backtest data and optimization results

---

## Repository Structure

```text
ema_backtest_project
├── .venv
├── data
│   ├── plots
│   │   ├── equity_curves.png
│   │   └── price_ema_signals.png
│   └── raw
│       ├── AAPL_prices.csv
│       └── ema_optimization_results.csv
├── src
│   ├── backtester.py
│   ├── config.py
│   ├── data_loader.py
│   ├── indicators.py
│   ├── metrics.py
│   ├── optimizer.py
│   ├── plots.py
│   ├── portfolio.py
│   └── signals.py
├── tests
├── main.py
├── README.md
└── requirements.txt