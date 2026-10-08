# Parte de caza de NevWorld

- En el archivo de referencia `nevworld_3345612477510823222_20260922_114341.jsonl` hay **6 eventos `hunt_completed`**. Uno tiene `event_index=407`, `tick=49225`, `villager_id=1884` y `prey_type="sheep"`. Son resultados de este archivo, no cifras exigibles a otras partidas.



| Necesidad | Selección | Motivo |
| --- | --- | --- |
| Cacería completada | `type == 'hunt_completed'` | Selecciona el hecho que interesa. |
| Aldeano | `villager_id` | Identifica quién la completó. |
| Presa | `prey_type` | Conserva el tipo de presa registrado. |
| Momento | `tick` | Sitúa el hecho en el tiempo simulado. |
| Partida | `run_id` | Separa registros de distintas sesiones. |
| Evento original | `run_id` y `event_index` | Permiten volver a la línea de origen. |

- activity describe otro tipo de evento; food_stock pertenece a las fotografías del mundo; amount_delta describe cambios de recursos. El evento de caza inspeccionado no contiene una cantidad de comida obtenida. No debemos inventarla ni atribuirle un cambio de recursos solo porque ocurra cerca en el tiempo.




Responde justificando cada decisión:

- Hay seis filas, por tanto hay seis cazadores distintos. ¿Es necesariamente cierto? No, puede ser el mismo, cada fila representa una cacería completa.

- Una fila indica que ese aldeano estuvo cazando durante todo el día. ¿Qué registra realmente la fila?
La fila registra un hecho en un tick, no incluye el inicio ni la duración de la cacería.

- Borro del DataFrame original todas las filas con algún NaN y después selecciono las cacerías. ¿Por qué puede desaparecer información válida?
Porque que tenga NaN no significa que sea inválido.

- El CSV está vacío, así que nadie intentó cazar. ¿Qué puedes afirmar realmente sobre el registro?
No hay cazas completas pero puede que alguien lo intentara.



## Solución de la ampliación

Investiga construction_abandoned y construction_expired. Esta vez necesitas dos tipos de evento en una tabla y debes conservar type para distinguirlos. Comprueba en el RAW si esos eventos incluyen building_id antes de darlo por supuesto:
- En el registro de referencia hay 4 construction_abandoned y 2 construction_expired. Los ejemplos inspeccionados aportan coordenadas, pero no building_id. La tabla debe conservar el tipo de evento para diferenciar ambos hechos.

Explica por qué dos registros con las mismas coordenadas no demuestran, por sí solos, que se trate de la misma obra:
- Dos sucesos pueden compartir coordenadas sin identificar una misma obra: el lugar puede reutilizarse. type conserva la categoría registrada, no explica por sí solo la causa detallada del abandono o de la caducidad.
