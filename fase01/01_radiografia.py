from pathlib import Path
import pandas as pd

# La ruta parte del proyecto, aunque ejecutes desde otra carpeta.
CARPETA_FASE = Path(__file__).resolve().parent
PROYECTO = CARPETA_FASE.parents[1]
DATASET = PROYECTO / 'data/raw/nevworld_7201485985000484657_20261005_182620.jsonl'

if not DATASET.exists():
    raise FileNotFoundError(f'No se encuentra: {DATASET.resolve()}')

# La semilla y el identificador de sesión se conservan como texto.
df = pd.read_json(DATASET, lines=True, dtype={'seed': 'string', 'run_id': 'string'})

# Validar antes de consultar columnas y posiciones.
required = ['run_id', 'event_index', 'tick', 'type']
assert not df.empty, 'El dataset está vacío'
assert all(column in df.columns for column in required), 'Faltan columnas principales'
assert not df.duplicated(['run_id', 'event_index']).any(), 'Hay eventos duplicados'

ordered = df.sort_values('event_index')
assert ordered['tick'].is_monotonic_increasing, 'Los ticks retroceden'
print('VALIDACIÓN BÁSICA: OK')

print('\nARCHIVO')
print(DATASET.name)

filas, columnas = df.shape
print('\nTAMAÑO Y COLUMNAS')
print('Eventos:', filas)
print('Columnas:', columnas)
print(df.columns.tolist())

print('Tipo del primer evento:', df['type'].iloc[0])


print('\nEVENTOS POR TIPO')
recuento = df['type'].value_counts()
print(recuento)
tipo_mas_frecuente = recuento.index[0]
cantidad_mas_frecuente = int(recuento.iloc[0])
print('Tipo más frecuente:', tipo_mas_frecuente)
print('Cantidad:', cantidad_mas_frecuente)

print('\nSESIÓN Y TIEMPO')
print('run_id:', df['run_id'].iloc[0])
print('Semilla:', df['seed'].iloc[0])
print('Esquema:', df['schema_version'].iloc[0])
print('Tick mínimo:', df['tick'].min())
print('Tick máximo:', df['tick'].max())
