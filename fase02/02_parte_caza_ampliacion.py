from pathlib import Path
import pandas as pd

CARPETA_FASE = Path(__file__).resolve().parent
PROYECTO = CARPETA_FASE.parents[1]
DATASET = PROYECTO / 'data/raw/nevworld_7201485985000484657_20261005_182620.jsonl'
OUTPUT_DIR = PROYECTO / 'data/processed'
if not DATASET.exists():
    raise FileNotFoundError(f'No se encuentra: {DATASET.resolve()}')
df = pd.read_json(DATASET, lines=True)


base = ['run_id', 'event_index', 'tick']
assert all(column in df.columns for column in [*base, 'type']), \
    'Faltan columnas principales del registro'


def event_table(event_type, columns):
    selected = [*base, *columns]
    available = [column for column in selected if column in df.columns]
    table = df.loc[df['type'] == event_type, available].copy()
    table = table.reindex(columns=selected)
    table['simulation_day'] = table['tick'] // 12000
    return table

#### AMPLIACIÓN: extraer construcciones abandonadas o caducadas.

# Estos son los dos tipos de evento que queremos conservar del RAW.
types = ['construction_abandoned', 'construction_expired']
# *base incorpora run_id, event_index y tick; añadimos el tipo y la celda.
columns = [*base, 'type', 'cell_x', 'cell_y']
# isin() marca con True cada fila cuyo tipo está en la lista anterior (o abandonadas o expiradas)
mask = df['type'].isin(types)
# loc filtra las filas; reindex ordena las columnas y crea las ausentes con NaN.
incidents = df.loc[mask].reindex(columns=columns).copy()
# Dividimos los ticks entre 12000 con división entera: el primer día es el 0.
incidents['simulation_day'] = incidents['tick'] // 12000

# sum() cuenta los True de mask: deben coincidir con las filas seleccionadas.
assert len(incidents) == mask.sum(), \
    'El número de incidencias de construcción no coincide'
# La pareja run_id/event_index debe ser única; any() detecta alguna repetición.
assert not incidents.duplicated(['run_id', 'event_index']).any(), \
    'Hay incidencias de construcción duplicadas'
# Comprobamos los campos obligatorios cuando hay incidencias que revisar.
if not incidents.empty:
    # notna() comprueba las celdas; los dos all() revisan columnas y tabla completa.
    assert incidents[columns].notna().all().all(), \
        'Hay incidencias de construcción con campos obligatorios ausentes'
# Todas las filas deben pertenecer a uno de los dos tipos de construcción.
assert incidents['type'].isin(types).all(), \
    'Hay tipos de evento no permitidos en las incidencias de construcción'

# Guardamos el CSV en la carpeta de salida ya creada, sin el índice de pandas.
incidents.to_csv(OUTPUT_DIR / 'construction_incidents.csv', index=False)
# Mostramos cuántas incidencias se han exportado.
print('construction_incidents ->', len(incidents), 'filas')
