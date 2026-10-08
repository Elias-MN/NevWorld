from pathlib import Path
import pandas as pd


#### 1. Leer el RAW y crear data/processed si hace falta.

CARPETA_FASE = Path(__file__).resolve().parent
PROYECTO = CARPETA_FASE.parents[1]
DATASET = PROYECTO / 'data/raw/nevworld_7201485985000484657_20261005_182620.jsonl'

OUTPUT_DIR = Path('data/processed')

if not DATASET.exists():
    raise FileNotFoundError(f'No se encuentra: {DATASET.resolve()}')

df = pd.read_json(DATASET, lines=True)

#### 3. Conservar run_id, event_index y tick, que la función añade automáticamente.

base = ['run_id', 'event_index', 'tick']
assert all(column in df.columns for column in [*base, 'type']), \
    'Faltan columnas principales del registro'


def event_table(event_type, columns):
    # event_type indica el tipo de evento que queremos extraer.
    # columns contiene los campos específicos que queremos conservar.
    # * desempaqueta las listas: juntamos los campos base con los específicos.
    selected = [*base, *columns]

    # Seleccionamos solo columnas que existen en el dataframe
    available = [column for column in selected if column in df.columns]

    # .loc filtra las filas del tipo indicado y conserva las columnas disponibles.
    # .copy() crea una tabla independiente para trabajar sin modificar df.
    table = df.loc[df['type'] == event_type, available].copy()

    # reindex(columns=selected) hace que table tenga exactamente las columnas de selected, en ese orden.
    # Las columnas que faltan se crean con valores ausentes (NaN).
    table = table.reindex(columns=selected)

    #### 4. Añadir simulation_day mediante tick // 12000

    # Cada día simulado tiene 12000 ticks; // calcula la división entera.
    # También crea la columna simulation_day cuando no hay filas.
    table['simulation_day'] = table['tick'] // 12000

    return table


#### 2. Seleccionar únicamente cacerías completadas y los campos justificados en tu ficha.

# Extraemos las cacerías completadas, identificando al aldeano y el tipo de presa.
# La función añade los campos base y el día simulado automáticamente.
hunts = event_table('hunt_completed', ['villager_id', 'prey_type'])

# Estos campos deben tener un valor en cada cacería registrada.
required = [*base, 'villager_id', 'prey_type']

# Cada assert comprueba una condición y detiene el programa con el mensaje
# indicado si no se cumple, antes de guardar un CSV con datos incorrectos.
# La comparación genera True/False; sum() cuenta los True del RAW.
# Ese recuento debe coincidir con el número de filas de la tabla de cacerías.
assert len(hunts) == (df['type'] == 'hunt_completed').sum(), \
    'El número de cacerías no coincide'

# duplicated() marca las repeticiones de la pareja partida/evento.
# any() detecta si hay alguna; not exige que no exista ninguna repetición.
assert not hunts.duplicated(['run_id', 'event_index']).any(), \
    'Hay eventos duplicados'

# Revisamos los valores obligatorios solo si la tabla contiene filas.
if not hunts.empty:
    # notna() marca las celdas con valor. El primer all() comprueba cada columna
    # y el segundo comprueba que todas las columnas hayan pasado la validación.
    # Crear columnas vacías con reindex() no soluciona datos obligatorios ausentes.
    assert hunts[required].notna().all().all(), \
        'Hay cacerías con campos obligatorios ausentes'

# Comprobamos el cálculo del día en todas las filas.
# Si no hay filas, all() devuelve True: no hay ningún cálculo incorrecto.
assert (hunts['simulation_day'] == hunts['tick'] // 12000).all(), \
    'El día calculado es incorrecto'

#### 5. Guardar data/processed/hunts.csv sin exportar el índice de pandas.

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
output = OUTPUT_DIR / 'hunts.csv'
hunts.to_csv(output, index=False)

#### 6. Mostrar la ruta del archivo generado y su número de filas.

print(output.resolve(), '->', len(hunts), 'filas')
# incidents.to_csv(OUTPUT_DIR / 'construction_incidents.csv', index=False)
# print('construction_incidents ->', len(incidents), 'filas')
