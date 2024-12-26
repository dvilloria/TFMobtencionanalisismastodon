# TFMobtencionanalisismastodon
Este repositorio tiene el código empleado para realizar el TFM

El archivo CreacionBD.py tiene el código para crear la base de datos general. Si se quiere replicar se deben cambiar los parámetros de conexión a la base de datos según los de cada usuario.

El archivo CreacionGrafo.py tiene el código para crear el grafo con las instancias y crea la tabla de instancias_reales en la BD. Al igual que en la anterior se deben configurar los parámetros de conexión a la base de datos.

El script nested.py calcula el nestedness de la red.

El archivo core-peri.py calcula el coreness de cada instancia y crea una imágen del grafo mostrando el core de l red y la periferia.

El archivo analisis.py contiene todo el código utilizado para realizar el análisis de la red.

Por último el archivo grafigrafo.py crea una imágen del grafo donde el tamaño del nodo va según su grado total a mayor grado más tamaño y su color según su nivel de intermediación.
