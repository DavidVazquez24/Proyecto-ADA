# Proyecto-ADA

"Optimización de Transferencia de Archivos en una VPN con Algoritmos Voraces"

Para la configuracion de la VPN se utilizo el software "Hamachi".
Dentro de Hamachi se puede crear una VPN a la cual se pueden unir otros dispositivos. Para ello, necesitan tener el identificador y la contraseña de red. Cada vez que un dispositivo se une a la VPN, Hamachi se encarga de colocarle una dirección IP estática; mediante dicha IP, se pueden empezar a hacer mediciones de red.

Para crear los grafos se necesiaton medir las latencias para esto se usaron scripts de python con la libreria "ping3" la cual hace ping a cada una de las IPs y las aristas de los grafos son el peso de cada arista y los nodos las respectivas conexiones ,para la creacion de los grafos es necesario la libreria networkx la cual facilita toda la implementacion de Dijkstra con metodos muy especificos ,al igual que para el ancho de banda se usa iperf3 desde la cmd.

En Python se utilizan las librerías tkinter, os y socket para la creación de la interfaz gráfica (GUI). Para seleccionar el archivo que se desea enviar, se emplea filedialog, y una vez elegido el archivo, es obligatorio seleccionar tanto la IP emisora (propia) como la receptora, asegurando que no sean iguales. Además, con las mediciones de red y el uso de grafos, se implementan los algoritmos de Dijkstra y Kruskal, ubicados en la carpeta src. Kruskal emplea mediciones hardcodeadas de ancho de banda, mientras que Dijkstra genera mediciones de latencia dinámicamente en cada ejecución del script. Este último está integrado con una GUI que permite seleccionar un archivo y elegir los nodos de origen y destino para su envío.
