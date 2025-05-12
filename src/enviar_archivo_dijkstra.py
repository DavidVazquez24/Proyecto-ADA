import tkinter as tk
from tkinter import filedialog
#from index import *
import heapq
from ping3 import ping 
from tkinter import messagebox as mb
from tkinter import ttk
import socket
import os

class GUI:
    
    anchoVentana=900
    altoVentana=600
    pings = {
    "Raul": "25.4.219.19",
    "Moy": "25.54.198.46",
    "David": "25.58.36.130"
    }
    def dijkstra(grafo, inicio, fin):
        distancias = {nodo: float('inf') for nodo in grafo}
        distancias[inicio] = 0
        anterior = {}
        cola = [(0, inicio)]

        while cola:
            distancia_actual, nodo_actual = heapq.heappop(cola)

            if nodo_actual == fin:
                break

            for vecino, peso in grafo[nodo_actual].items():
                nueva_distancia = distancia_actual + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anterior[vecino] = nodo_actual
                    heapq.heappush(cola, (nueva_distancia, vecino))

        # Reconstruir camino
        camino = []
        actual = fin
        while actual in anterior:
            camino.insert(0, actual)
            actual = anterior[actual]
        if camino:
            camino.insert(0, inicio)

        return camino, distancias[fin]
    
    def construir_grafo_latencias(pings):
        grafo = {nombre: {} for nombre in pings}
        for origen, ip_origen in pings.items():
            for destino, ip_destino in pings.items():
                if origen == destino:
                    continue
                latency = ping(ip_destino, timeout=2)
                if latency:
                    grafo[origen][destino] = latency * 1000  # ms
                else:
                    print(f"Sin respuesta: {origen} -> {destino}")
        return grafo
    
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

        # Construir el grafo y aplicar Dijkstra
        grafo = GUI.construir_grafo_latencias(GUI.pings)
        camino, costo = GUI.dijkstra(grafo, emisor_nombre, receptor_nombre)

        if not camino or len(camino) < 2:
            mb.showerror("Error", "No se encontró un camino entre emisor y receptor")
            return

        siguiente_salto = camino[1]  # Nodo siguiente en la ruta
        ip_destino = GUI.pings[siguiente_salto]
        puerto = 5201  # Asegúrate de que el receptor use este puerto

        try:
            with socket.socket() as s:
                s.connect((ip_destino, puerto))
                s.send(os.path.basename(self.archivo).encode())  # Enviar nombre del archivo
                with open(self.archivo, 'rb') as f:
                    while True:
                        datos = f.read(1024)
                        if not datos:
                            break
                        s.send(datos)
            mb.showinfo("Éxito", f"Archivo enviado a {siguiente_salto} ({ip_destino})\nRuta: {' ➜ '.join(camino)}\nLatencia total estimada: {costo:.2f} ms")
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