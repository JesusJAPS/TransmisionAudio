import socket
import threading
import signal
import sys

# Función para manejar la conexión con un cliente
def handle_client(conn, addr):
    print(f'Conexión establecida desde {addr}')
    while True:
        data = conn.recv(1024).decode()  # Decodifica los datos recibidos del cliente
        if data == 'exit':
            conn.close()
            break
        print(f'Comando recibido: {data}')
        if data == 'play':
            conn.sendall(b'play')  # Envía la señal de reproducción al cliente
        elif data == 'pause':
            conn.sendall(b'pause')  # Envía la señal de pausa al cliente
        elif data == 'unpause':
            conn.sendall(b'unpause')  # Envía la señal de reanudación al cliente
        elif data == 'stop':
            conn.sendall(b'stop')  # Envía la señal de parada al cliente

# Creación del socket del servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 12345))  # Enlaza el socket a todas las interfaces en el puerto 12345
sock.listen()  # Habilita la escucha de conexiones entrantes

# Función para cerrar el servidor correctamente al recibir una señal SIGINT (Ctrl+C)
def close_server(signal, frame):
    print("\nCerrando el servidor...")
    sock.close()
    sys.exit(0)

# Maneja la señal SIGINT (Ctrl+C) para cerrar el servidor correctamente
signal.signal(signal.SIGINT, close_server)

# Bucle principal para aceptar conexiones entrantes y manejarlas en hilos separados
while True:
    try:
        conn, addr = sock.accept()  # Acepta una nueva conexión entrante
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))  # Crea un hilo para manejar el cliente
        client_thread.start()  # Inicia el hilo
    except Exception as e:
        print(f'Error: {e}')
