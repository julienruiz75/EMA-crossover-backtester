import pandas as pd


def run_backtest(
    df: pd.DataFrame,
    initial_capital: float,
    transaction_cost: float,
    slippage: float
) -> pd.DataFrame:
    """
    Exécute un backtest simple long/flat.

    Hypothèses :
    - position = 1 : investi sur l'actif
    - position = 0 : cash
    - coûts appliqués lors des changements de position

    Args:
        df: DataFrame contenant Close, position et trade
        initial_capital: capital initial
        transaction_cost: coût proportionnel par changement de position
        slippage: slippage proportionnel par changement de position

    Returns:
        DataFrame enrichi avec rendements et courbes de capital
    """
    data = df.copy()

    # Rendement journalier du sous-jacent
    data["asset_return"] = data["Close"].pct_change().fillna(0)

    # Rendement brut de la stratégie
    data["strategy_gross_return"] = data["position"] * data["asset_return"]

    # Coût total appliqué uniquement lors d'un trade
    total_cost = transaction_cost + slippage
    data["cost"] = data["trade"] * total_cost

    # Rendement net de la stratégie
    data["strategy_net_return"] = data["strategy_gross_return"] - data["cost"]

    # Courbes de capital
    data["buy_and_hold_equity"] = initial_capital * (1 + data["asset_return"]).cumprod()
    data["strategy_equity"] = initial_capital * (1 + data["strategy_net_return"]).cumprod()

    return data