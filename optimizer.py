import pandas as pd

from src.indicators import add_ema_columns
from src.signals import generate_ema_signals
from src.backtester import run_backtest
from src.metrics import compute_performance_metrics


def run_parameter_grid_search(
    df: pd.DataFrame,
    short_windows: list[int],
    long_windows: list[int],
    initial_capital: float,
    transaction_cost: float,
    slippage: float,
    annual_trading_days: int
) -> pd.DataFrame:
    """
    Teste plusieurs combinaisons EMA courte / EMA longue
    et renvoie un tableau de résultats.
    """
    results = []

    for short_window in short_windows:
        for long_window in long_windows:
            if short_window >= long_window:
                continue

            data_with_emas = add_ema_columns(
                df=df,
                short_window=short_window,
                long_window=long_window
            )

            data_with_signals = generate_ema_signals(
                df=data_with_emas,
                short_window=short_window,
                long_window=long_window
            )

            backtest_results = run_backtest(
                df=data_with_signals,
                initial_capital=initial_capital,
                transaction_cost=transaction_cost,
                slippage=slippage
            )

            metrics = compute_performance_metrics(
                df=backtest_results,
                annual_trading_days=annual_trading_days
            )

            results.append({
                "short_ema": short_window,
                "long_ema": long_window,
                "total_return": metrics["Total Return"],
                "cagr": metrics["CAGR"],
                "annual_volatility": metrics["Annual Volatility"],
                "sharpe_ratio": metrics["Sharpe Ratio"],
                "max_drawdown": metrics["Max Drawdown"],
                "number_of_trades": metrics["Number of Trades"]
            })

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by="sharpe_ratio", ascending=False).reset_index(drop=True)

    return results_df