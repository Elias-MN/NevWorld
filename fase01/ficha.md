# Radiografía de mi partida de NevWorld

| Dato de mi partida | Resultado |
| --- | --- |
| Nombre del archivo JSONL | `nevworld_7201485985000484657_20261005_182620.jsonl` |
| Número total de eventos | 1437 |
| Número de columnas | 34 |
| Nombres de las columnas | `schema_version`<br>`run_id`<br>`seed`<br>`event_index`<br>`tick`<br>`type`<br>`started_at_utc`<br>`building_id`<br>`building_type`<br>`cell_x`<br>`cell_y`<br>`width`<br>`height`<br>`villager_id`<br>`activity`<br>`resource_type`<br>`population`<br>`constructed_buildings`<br>`wood_stock`<br>`food_stock`<br>`gold_stock`<br>`day`<br>`amount_before`<br>`amount_after`<br>`amount_delta`<br>`actor_id`<br>`target_id`<br>`interaction_type`<br>`topic`<br>`relationship_actor_to_target_after`<br>`relationship_target_to_actor_after`<br>`need_type`<br>`state`<br>`prey_type` |
| Tipo del primer evento registrado | `simulation_started` |
| Tipo de evento más frecuente y cantidad | `villager_activity_changed`: 1169 |
| Recuento de todos los tipos de evento | `villager_activity_changed`: 1169<br>`world_snapshot`: 70<br>`villager_need_changed`: 58<br>`social_interaction`: 53<br>`resource_changed`: 52<br>`villager_drank`: 12<br>`villager_ate`: 8<br>`construction_abandoned`: 5<br>`building_created`: 4<br>`construction_expired`: 4<br>`simulation_started`: 1<br>`hunt_completed`: 1 |
| `run_id`, semilla y versión del esquema de la primera fila | `run_id`: `20261005_182620_7201485985000484657_0a8009aed3d743b6ac6a6d16ba9acfdd`<br>Semilla: `7201485985000484657`<br>Esquema: 2 |
| Tick mínimo y tick máximo | Mínimo: 0<br>Máximo: 42080 |
| Resultado de las validaciones | **Las cuatro pasan:** tabla no vacía; columnas principales presentes; pareja `run_id` + `event_index` sin duplicados; ticks sin retrocesos al ordenar por `event_index`. |

### 1. ¿Qué permite afirmar el recuento? ¿Por qué el tipo más frecuente no tiene que ser el más importante?

En esta partida se registraron 1437 eventos de 12 tipos diferentes. El tipo más frecuente es `villager_activity_changed`, con 1169 registros.
- El recuento describe cuántas veces aparece cada tipo en el archivo, no mide cuánto duran las actividades ni su impacto.
- Un evento poco frecuente, como el inicio de la simulación o la creación de un edificio, puede ser importante para comprender lo ocurrido.

### 2. ¿Por qué una celda vacía no significa necesariamente que el registro esté mal?

- Los eventos no tienen todos los mismos campos.
- Una ausencia debe interpretarse según el evento; no equivale automáticamente a un error ni a un valor cero.

### 3. ¿Qué sé ahora del archivo y qué pregunta necesitaría un análisis posterior?

- Ahora conocemos el tamaño, los campos, las frecuencias y el intervalo de ticks del archivo. Una pregunta posterior podría ser cómo cambió la población durante la partida, cuantos aldeanos nos han dejado por el camino...


