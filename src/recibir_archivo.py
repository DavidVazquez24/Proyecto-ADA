import socket
import os

# Diccionario de nombres a IPs
pings = {
    "Raul": "25.4.219.19",
    "Moy": "25.54.198.46",
    "David": "25.58.36.130",
    "Sergio": "25.59.171.8"
}

nombre_nodo = "David" 

def recibir_y_reenviar():
    puerto = 5201
    with socket.socket() as servidor:
        servidor.bind(('', puerto))
        servidor.listen(1)
        print(f"[{nombre_nodo}] Esperando conexión en el puerto {puerto}...")

        conn, addr = servidor.accept()
        with conn:
            print(f"[{nombre_nodo}] Conexión desde {addr}")

            # Recibir el nombre del archivo
            nombre_archivo = conn.recv(1024).decode()
            conn.send(b"ACK")  # Confirmación

            # Recibir la ruta restante
            ruta_str = conn.recv(1024).decode()
            ruta = ruta_str.split(",")
            conn.send(b"ACK")  # Confirmación

            print(f"[{nombre_nodo}] Ruta recibida: {' ➜ '.join(ruta)}")

            # Recibir archivo
            with open(nombre_archivo, 'wb') as f:
                while True:
                    datos = conn.recv(1024)
                    if datos == b"DONE":
                        break
                    f.write(datos)

            print(f"[{nombre_nodo}] Archivo recibido: {nombre_archivo}")

            # Si soy el destino final, guardar y terminar
            if ruta[0] == nombre_nodo and len(ruta) == 1:
                print(f"[{nombre_nodo}] Soy el destino final. Archivo guardado.")
                return
            else:
                # Reenviar al siguiente nodo en la ruta
                siguiente = ruta[1]  # ruta[0] soy yo, ruta[1] es el siguiente
                ruta_restante = ruta[1:]
                ip_destino = pings[siguiente]

                print(f"[{nombre_nodo}] Reenviando a {siguiente} ({ip_destino})...")

                with socket.socket() as s:
                    s.connect((ip_destino, puerto))
                    s.send(nombre_archivo.encode())
                    s.recv(1024)
                    s.send(",".join(ruta_restante).encode())
                    s.recv(1024)

                    with open(nombre_archivo, 'rb') as f:
                        while True:
                            datos = f.read(1024)
                            if not datos:
                                break
                            s.send(datos)
                    s.send(b"DONE")

                print(f"[{nombre_nodo}] Archivo reenviado a {siguiente}")

if __name__ == "__main__":
    while True:
        recibir_y_reenviar()
