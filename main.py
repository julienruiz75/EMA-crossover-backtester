from src.config import BacktestConfig
from src.data_loader import download_price_data, clean_price_data, save_data_to_csv
from src.indicators import add_ema_columns
from src.signals import generate_ema_signals
from src.backtester import run_backtest
from src.metrics import compute_performance_metrics
from src.plots import plot_price_and_emas, plot_equity_curves
from src.optimizer import run_parameter_grid_search


def main() -> None:
    config = BacktestConfig()

    raw_data = download_price_data(
        symbol=config.symbol,
        start_date=config.start_date,
        end_date=config.end_date
    )

    clean_data = clean_price_data(raw_data)

    # =========================
    # Backtest principal
    # =========================
    data_with_emas = add_ema_columns(
        df=clean_data,
        short_window=config.short_ema_window,
        long_window=config.long_ema_window
    )

    data_with_signals = generate_ema_signals(
        df=data_with_emas,
        short_window=config.short_ema_window,
        long_window=config.long_ema_window
    )

    backtest_results = run_backtest(
        df=data_with_signals,
        initial_capital=config.initial_capital,
        transaction_cost=config.transaction_cost,
        slippage=config.slippage
    )

    output_path = f"data/raw/{config.symbol}_prices.csv"
    save_data_to_csv(backtest_results, output_path)

    metrics = compute_performance_metrics(
        df=backtest_results,
        annual_trading_days=config.annual_trading_days
    )

    print("Backtest principal terminé.\n")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")

    plot_price_and_emas(
        df=backtest_results,
        short_window=config.short_ema_window,
        long_window=config.long_ema_window
    )

    plot_equity_curves(backtest_results)

    # =========================
    # Optimisation des paramètres EMA
    # =========================
    short_windows = [10, 20, 30, 50]
    long_windows = [80, 100, 150, 200]

    optimization_results = run_parameter_grid_search(
        df=clean_data,
        short_windows=short_windows,
        long_windows=long_windows,
        initial_capital=config.initial_capital,
        transaction_cost=config.transaction_cost,
        slippage=config.slippage,
        annual_trading_days=config.annual_trading_days
    )

    optimization_output_path = "data/raw/ema_optimization_results.csv"
    save_data_to_csv(optimization_results, optimization_output_path)

    print("\nTop 10 des meilleures combinaisons EMA par Sharpe Ratio :\n")
    print(optimization_results.head(10))

    print(f"\nRésultats d'optimisation sauvegardés dans : {optimization_output_path}")


if __name__ == "__main__":
    main()