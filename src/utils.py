from typing import Optional
from pathlib import Path
import pandas as pd


def load_data(base_dir: Path) -> dict:
    """
    Carga los archivos desde la carpeta data/. Retorna un diccionario con los dataframes.
    """
    data_dir = base_dir / "data"
    return {
        "trips": pd.read_excel(data_dir / "bus_data.xlsx"),
        "coor": pd.read_excel(data_dir / "coordenadas_1.xlsx", header=1),
        "org": pd.read_excel(data_dir / "origen-destino.xlsx", header=1),
    }


def match_terminal(lat: float, lon: float, bounds_df: pd.DataFrame, margin: float = 0.1) -> Optional[str]:
    """
    Devuelve el nombre del terminal si la coordenada está dentro de algún polígono de coordenadas con margen.
    """
    for _, row in bounds_df.iterrows():
        if (
            min(row['Lat1'], row['lat2']) - margin <= lat <= max(row['Lat1'], row['lat2']) + margin and
            min(row['long1'], row['long2']) - margin <= lon <= max(row['long1'], row['long2']) + margin
        ):
            return row['terminal_name']
    return None