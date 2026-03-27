from dataclasses import dataclass


@dataclass
class BacktestConfig:
    """
    Configuration principale du projet de backtest EMA crossover.
    """

    symbol: str = "AAPL"
    start_date: str = "2015-01-01"
    end_date: str = "2025-01-01"

    short_ema_window: int = 20
    long_ema_window: int = 100

    initial_capital: float = 10_000.0

    transaction_cost: float = 0.001
    slippage: float = 0.0005

    annual_trading_days: int = 252