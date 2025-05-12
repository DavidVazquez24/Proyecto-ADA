from ping3 import ping 

# Diccionario con nombres y sus IPs de Hamachi
pings = {"Raul": "25.4.219.19",
         "Moy": "25.54.198.46",
         "Sergio": "25.59.171.8",
         "David": "25.58.36.130"}

# Medir latencia
def latencias(pings):
    print("---- Latencias ----")
    for host, ip in pings.items():
        try:
            latency = ping(ip, timeout=2)  # Timeout de 2 segundos
            if latency is not None:
                print(f"Latencia a {host} ({ip}): {latency * 1000:.2f} ms")
            else:
                print(f"No se pudo alcanzar {host} ({ip})")
        except Exception as e:
            print(f"Error al hacer ping a {host}: {e}")

latencias(pings)