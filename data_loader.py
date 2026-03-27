from pathlib import Path
import pandas as pd
import yfinance as yf


def download_price_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Télécharge les données historiques d'un actif avec yfinance.
    """
    df = yf.download(symbol, start=start_date, end=end_date, auto_adjust=False)

    if df.empty:
        raise ValueError(f"Aucune donnée téléchargée pour {symbol}.")

    df = df.reset_index()
    return df


def clean_price_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les données téléchargées et conserve les colonnes utiles.
    """
    required_columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]

    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Colonnes manquantes : {missing_cols}")

    clean_df = df[required_columns].copy()
    clean_df = clean_df.dropna()
    clean_df["Date"] = pd.to_datetime(clean_df["Date"])
    clean_df = clean_df.sort_values("Date").reset_index(drop=True)

    return clean_df


def save_data_to_csv(df: pd.DataFrame, file_path: str) -> None:
    """
    Sauvegarde le DataFrame dans un fichier CSV.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)