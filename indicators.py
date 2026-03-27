import pandas as pd


def add_ema_columns(
    df: pd.DataFrame,
    short_window: int,
    long_window: int
) -> pd.DataFrame:
    """
    Ajoute deux colonnes EMA au DataFrame :
    - EMA courte
    - EMA longue

    Args:
        df: DataFrame contenant les prix
        short_window: fenêtre de l'EMA courte
        long_window: fenêtre de l'EMA longue

    Returns:
        DataFrame enrichi avec les colonnes EMA
    """

    # On travaille sur une copie pour éviter de modifier le DataFrame original directement
    data = df.copy()

    # Vérification simple : la fenêtre courte doit être strictement inférieure à la longue
    if short_window >= long_window:
        raise ValueError("La fenêtre courte doit être inférieure à la fenêtre longue.")

    # Calcul de l'EMA courte sur la colonne 'Close'
    data[f"EMA_{short_window}"] = data["Close"].ewm(
        span=short_window,
        adjust=False
    ).mean()

    # Calcul de l'EMA longue sur la colonne 'Close'
    data[f"EMA_{long_window}"] = data["Close"].ewm(
        span=long_window,
        adjust=False
    ).mean()

    return data