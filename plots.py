import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def plot_price_and_emas(
    df: pd.DataFrame,
    short_window: int,
    long_window: int
) -> None:
    """
    Sauvegarde le graphique du prix, des EMA, et des signaux d'entrée/sortie.
    """
    plt.figure(figsize=(15, 8))

    plt.plot(df["Date"], df["Close"], label="Close")
    plt.plot(df["Date"], df[f"EMA_{short_window}"], label=f"EMA {short_window}")
    plt.plot(df["Date"], df[f"EMA_{long_window}"], label=f"EMA {long_window}")

    entries = df[df["trade"] == 1]
    entry_points = entries[entries["position"] == 1]
    exit_points = entries[entries["position"] == 0]

    plt.scatter(
        entry_points["Date"],
        entry_points["Close"],
        marker="^",
        s=100,
        label="Buy Signal"
    )

    plt.scatter(
        exit_points["Date"],
        exit_points["Close"],
        marker="v",
        s=100,
        label="Sell Signal"
    )

    plt.title("Prix, EMA et signaux d'entrée/sortie")
    plt.xlabel("Date")
    plt.ylabel("Prix")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_dir = Path("data/plots")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / "price_ema_signals.png", dpi=300)
    plt.close()


def plot_equity_curves(df: pd.DataFrame) -> None:
    """
    Sauvegarde la courbe de capital stratégie vs buy-and-hold.
    """
    plt.figure(figsize=(14, 7))
    plt.plot(df["Date"], df["strategy_equity"], label="EMA Strategy Equity")
    plt.plot(df["Date"], df["buy_and_hold_equity"], label="Buy and Hold Equity")
    plt.title("Comparaison des courbes de capital")
    plt.xlabel("Date")
    plt.ylabel("Capital")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_dir = Path("data/plots")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / "equity_curves.png", dpi=300)
    plt.close()