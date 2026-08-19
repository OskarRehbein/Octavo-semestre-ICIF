# Laberinto creado a base de Gemini y Claude

## Comparación BFS vs DFS

| Semilla | Algoritmo | Celdas expandidas | Pasos del camino |
|---------|-----------|--------------------|-------------------|
|   31      |    BFS    | 183               | 66               |
|   31      |    DFS    | 162               | 72               |
|   45      |    BFS    | 136               | 71               |
|   45      |    DFS    | 120               | 71               |
|   65      |    BFS    | 278               | 80               |
|   65      |    DFS    | 173               | 96               |

### Conclusion

* A partir de los datos recolectados, se puede ver como BFS realiza una busqueda extensiva pasando nivel a nivel, siendo esto mas evidente en el caso de la semilla 65, por lo mismo BFS siempre llega a la solucion optiva, donde solo el caso de la semilla 45 DFS fue capaz de encontrar la solucion optima (Los recorridos son distintos pero el numero de pasos es el mismo) aunque este llegue a una solucion expandiendo menos celdas en todos los casos analizados.


## Datos de comparacion extra

| Semilla | Algoritmo | Celdas expandidas | Pasos del camino |
|---------|-----------|--------------------|-------------------|
|   98      |    BFS    | 219               | 51               |
|   98      |    DFS    | 92                | 63               |
|   93      |    BFS    | 198               | 44               |
|   93      |    DFS    | 188               | 74               |
|   17      |    BFS    | 124               | 53               |
|   17      |    DFS    | 95                | 71               |

* Se repiten las tendencia mencionadas en la conclusion anterior.
