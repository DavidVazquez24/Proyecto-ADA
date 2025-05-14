import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb
from tkinter import ttk
import socket
import os
import networkx  as nx
import matplotlib.pyplot as plt

class GUI:
    
    anchoVentana=900
    altoVentana=600

    #IPs de la VPN
    pings = {
    "Raul": "25.4.219.19",
    "Moy": "25.54.198.46",
    "David": "25.58.36.130",
    "Sergio": "25.59.171.8"
    }
    #Medidas de latencia promedio
    latencias= [
    ('Moy', 'David', 30),
    ('Moy', 'Raul', 29),
    ('Moy', 'Sergio', 30),
    ('David', 'Moy', 36),
    ('David', 'Raul', 14),
    ('David', 'Sergio', 102),
    ('Raul', 'Moy', 33),
    ('Raul', 'David', 10),
    ('Raul', 'Sergio', 255),
    ('Sergio', 'Moy', 31),
    ('Sergio', 'David', 116),
    ('Sergio', 'Raul', 270),
    ]
    
    def enviar(self):
        emisor = self.listaIPEmisor.get()
        receptor = self.listaIPReceptor.get()
        self.listaIPEmisor.set("")
        self.listaIPReceptor.set("")

        if not emisor or not receptor:
            mb.showerror("ERROR", "No hay selección")
            return
        elif emisor == receptor:
            mb.showerror("ERROR", "Las IPs son idénticas")
            return
        if not self.archivo:
            mb.showerror("ERROR", "No hay ningún archivo seleccionado")
            return

        emisor_nombre = emisor.split()[0]
        receptor_nombre = receptor.split()[0]

        # Construir grafo
        grafo = nx.Graph()
        grafo.add_weighted_edges_from(GUI.latencias)

        try:
            camino = nx.dijkstra_path(grafo, source=emisor_nombre, target=receptor_nombre)
            costo = nx.dijkstra_path_length(grafo, source=emisor_nombre, target=receptor_nombre)
        except nx.NetworkXNoPath:
            mb.showerror("ERROR", "No hay ruta entre los nodos seleccionados")
            return

        # Mostrar la ruta en un gráfico
        pos = nx.spring_layout(grafo, seed=42)
        plt.figure(figsize=(8, 6))
        nx.draw(grafo, pos, with_labels=True, node_color='lightblue', node_size=1000, font_weight='bold')
        labels = nx.get_edge_attributes(grafo, 'weight')
        labels = {k: f"{v:.1f} ms" for k, v in labels.items()}
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels)
        path_edges = list(zip(camino, camino[1:]))
        nx.draw_networkx_edges(grafo, pos, edgelist=path_edges, edge_color='red', width=3)
        plt.title(f"Ruta de {emisor_nombre} a {receptor_nombre} ({costo:.2f} ms)")
        plt.show()

        print("Ruta calculada:", camino)

        # Obtener el siguiente nodo y su IP
        siguiente_salto = camino[1]  # El primer salto después del emisor
        ruta_restante = camino[1:]  # Desde el primer nodo hasta el destino

        ip_destino = GUI.pings[siguiente_salto]
        puerto = 5201

        try:
            with socket.socket() as s:
                s.connect((ip_destino, puerto))
                # Enviar nombre del archivo
                s.send(os.path.basename(self.archivo).encode())
                s.recv(1024)  # Esperar confirmación

                # Enviar la ruta restante como cadena
                s.send(",".join(ruta_restante).encode())
                s.recv(1024)  # Esperar confirmación

                # Enviar el archivo por partes
                with open(self.archivo, 'rb') as f:
                    while True:
                        datos = f.read(1024)
                        if not datos:
                            break
                        s.send(datos)
                s.send(b"DONE")  # Señal de fin de archivo

            mb.showinfo("Éxito", f"Archivo: {self.archivo} enviado a {siguiente_salto} ({ip_destino})\nRuta: {' ➜ '.join(camino)}\nLatencia estimada: {costo:.2f} ms")
        except Exception as e:
            mb.showerror("Error", f"No se pudo enviar el archivo a {ip_destino}:\n{e}")

        self.archivo = ""
        self.etiquetaArchivo.config(text="Ningún archivo seleccionado")

    def seleccionar_archivo(self):
        self.archivo = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=[("Todos los archivos", "*.*"),("Archivos de texto", "*.txt") ]
        )
        if self.archivo:
            self.etiquetaArchivo.config(text=f"Seleccionado:{self.archivo}")

    def __init__(self):
        self.archivo=""
        self.root=tk.Tk()
        self.root.title("TITULO")
        self.root.geometry(f"900x600")
        x = (self.root.winfo_screenwidth() // 2) - (self.anchoVentana // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.altoVentana // 2)
        self.root.geometry(f"{self.anchoVentana}x{self.altoVentana}+{x}+{y}")
        self.root.resizable(False, False)

        
        self.framePrincipal=tk.Frame(self.root,bg="lightblue")
        self.framePrincipal.pack(expand=1,fill="both")


        self.frameEmisor=tk.Frame(self.framePrincipal,height=150,width=250,bg="lightskyblue4")
        self.frameEmisor.place(x=150,y=200)

        self.etiquetaEmisor=tk.Label(self.frameEmisor,text="Selecciona tu IP:",font=("Arial",15),bg="lightskyblue4")
        self.etiquetaEmisor.place(x=25,y=15)

        self.listaIPEmisor=ttk.Combobox(self.frameEmisor,values=["Raul 25.4.219.19","Moy 25.54.198.46","Sergio 25.59.171.8","David 25.58.36.130"])
        self.listaIPEmisor.place(x=40,y=60)


        self.frameReceptor=tk.Frame(self.framePrincipal,height=150,width=250,bg="lightskyblue4")
        self.frameReceptor.place(x=500,y=200)

        self.etiquetaReceptor=tk.Label(self.frameReceptor,text="Selecciona la IP destino:",font=("Arial",15),bg="lightskyblue4")
        self.etiquetaReceptor.place(x=25,y=15)

        self.listaIPReceptor=ttk.Combobox(self.frameReceptor,values=["Raul 25.4.219.19","Moy 25.54.198.46","Sergio 25.59.171.8","David 25.58.36.130"])
        self.listaIPReceptor.place(x=40,y=60)


        self.frameArchivo=tk.Frame(self.framePrincipal,height=100,width=430,bd=7,relief="ridge",bg="lightskyblue1")
        self.frameArchivo.place(x=250,y=450)

        self.etiquetaArchivo = tk.Label(self.frameArchivo, text="Ningún archivo seleccionado",bg="lightskyblue1")
        self.etiquetaArchivo.place(x=5,y=14)

        self.botonArchivo=tk.Button(self.frameArchivo,text="Seleccionar Archivo",command=self.seleccionar_archivo)
        self.botonArchivo.place(x=50,y=55)

        self.botonEnviar=tk.Button(self.frameArchivo,text="Enviar Archivo",command=self.enviar)#COMMAND
        self.botonEnviar.place(x=250,y=55)

        self.root.mainloop()


GUI()