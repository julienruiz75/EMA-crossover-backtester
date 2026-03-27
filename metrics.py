import pandas as pd
import numpy as np


def compute_performance_metrics(
    df: pd.DataFrame,
    annual_trading_days: int
) -> dict:
    """
    Calcule les principales métriques de performance de la stratégie.
    """
    strategy_returns = df["strategy_net_return"].copy()
    equity_curve = df["strategy_equity"].copy()

    total_return = equity_curve.iloc[-1] / equity_curve.iloc[0] - 1

    n_days = len(df)
    cagr = (equity_curve.iloc[-1] / equity_curve.iloc[0]) ** (annual_trading_days / n_days) - 1

    annual_vol = strategy_returns.std() * np.sqrt(annual_trading_days)

    if strategy_returns.std() == 0:
        sharpe = 0.0
    else:
        sharpe = (strategy_returns.mean() / strategy_returns.std()) * np.sqrt(annual_trading_days)

    rolling_max = equity_curve.cummax()
    drawdown = equity_curve / rolling_max - 1
    max_drawdown = drawdown.min()

    trade_count = int(df["trade"].sum())

    metrics = {
        "Total Return": total_return,
        "CAGR": cagr,
        "Annual Volatility": annual_vol,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_drawdown,
        "Number of Trades": trade_count
    }

    return metrics