import pandas as pd


def generate_ema_signals(
    df: pd.DataFrame,
    short_window: int,
    long_window: int
) -> pd.DataFrame:
    """
    Génère les signaux de trading à partir du croisement des EMA.

    Règle :
    - signal brut = 1 si EMA courte > EMA longue
    - signal brut = 0 sinon

    Puis on décale la position d'un jour pour éviter le look-ahead bias.

    Args:
        df: DataFrame contenant les colonnes EMA
        short_window: fenêtre EMA courte
        long_window: fenêtre EMA longue

    Returns:
        DataFrame enrichi avec signal et position
    """
    data = df.copy()

    short_col = f"EMA_{short_window}"
    long_col = f"EMA_{long_window}"

    if short_col not in data.columns or long_col not in data.columns:
        raise ValueError("Les colonnes EMA nécessaires sont absentes du DataFrame.")

    # Signal théorique observé à la clôture
    data["signal"] = (data[short_col] > data[long_col]).astype(int)

    # Position réellement tenue le jour suivant
    data["position"] = data["signal"].shift(1).fillna(0)

    # Variations de position utiles pour compter les trades et appliquer des coûts
    data["trade"] = data["position"].diff().abs().fillna(0)

    return data