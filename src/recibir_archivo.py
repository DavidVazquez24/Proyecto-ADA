import os
import socket

def recibir_archivo(puerto=5201, carpeta_destino="archivos_recibidos"):
    os.makedirs(carpeta_destino, exist_ok=True)

    with socket.socket() as s:
        s.bind(('', puerto))  # Escuchar en todas las interfaces
        s.listen(1)
        print(f"Esperando conexión en el puerto {puerto}...")

        conn, addr = s.accept()
        with conn:
            print(f"Conexión establecida desde {addr}")
            nombre_archivo = conn.recv(1024).decode()
            ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)

            with open(ruta_archivo, 'wb') as f:
                while True:
                    datos = conn.recv(1024)
                    if not datos:
                        break
                    f.write(datos)

            print(f"Archivo recibido: {ruta_archivo}")

recibir_archivo()