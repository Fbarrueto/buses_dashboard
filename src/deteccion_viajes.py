import pandas as pd
from typing import List, Tuple


def detectar_viajes(df: pd.DataFrame, rutas_validas: List[Tuple[str, str]]) -> pd.DataFrame:
    """
    Dado un DataFrame con paradas y una lista de rutas válidas, asigna trip_id a cada fila que pertenezca a un viaje.
    """
    df = df.sort_values(['VehicleID', 'Stop_Start']).reset_index(drop=True)
    df['terminal_norm'] = df['terminal_name'].str.lower().fillna('')

    trip_id = 0
    trip_ids = [None] * len(df)
    i = 0
    while i < len(df):
        origen_row = df.iloc[i]
        origen_terminal = origen_row['terminal_norm']

        if origen_terminal in [r[0] for r in rutas_validas]:
            j = i + 1
            while j < len(df):
                destino_row = df.iloc[j]
                destino_terminal = destino_row['terminal_norm']
                if destino_terminal != origen_terminal and (origen_terminal, destino_terminal) in rutas_validas:
                    trip_id += 1
                    for k in range(i, j + 1):
                        trip_ids[k] = trip_id
                    i = j  # avanzar al destino
                    break
                j += 1
        i += 1

    df['trip_id'] = trip_ids
    return df


def resumir_viajes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa por trip_id y resume los datos del viaje.
    """
    trip_summary = df.dropna(subset=['trip_id']).groupby('trip_id').agg(
        VehicleID=('VehicleID', 'first'),
        origen=('terminal_name', 'first'),
        destino=('terminal_name', 'last'),
        inicio=('Stop_Start', 'first'),
        fin=('Stop_Start', 'last'),
        duracion_minutos=('Stop_Start', lambda x: (x.max() - x.min()).total_seconds() / 60),
        num_paradas=('Stop_Start', 'count'),
        stop_duration_total_minutos=('Stop_Duration', lambda x: x.sum() / 60)
    ).reset_index()
    return trip_summary